"""Baseline numbers and what-if estimates for the refund case.
The cost assumptions are the constants near the top; change them and re-run.
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
A = ROOT / "analysis"
(A / "figures").mkdir(parents=True, exist_ok=True)
plt.rcParams.update({"figure.dpi": 120, "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.alpha": .25})

AGENT_COST_PER_HOUR = 20.0     # assumption: fully loaded support agent cost (currency units per hour)
PROACTIVE_CREDIT = 3.0         # assumption: automatic goodwill credit for a very late order
AUTO_LIMIT, AUTO_PRIOR_MAX = 10.0, 3
OUT = {}

d = pd.read_csv(ROOT / "data" / "orders.csv", parse_dates=["created_at"])
deliv = d[d.status == "Delivered"].copy()
canc = d[d.status == "Cancelled"].copy()
ref = d[d.refund_requested == 1].copy()
gmv = d.order_value.sum()

# ---------------------------------------------------------------- baseline
OUT["orders"] = len(d)
OUT["gmv"] = round(gmv)
OUT["delivered"] = len(deliv)
OUT["cancelled"] = len(canc)
OUT["cancel_rate_pct"] = round(100 * len(canc) / len(d), 1)
OUT["refund_cases"] = len(ref)
OUT["refund_rate_pct_of_delivered"] = round(100 * len(ref) / len(deliv), 1)
OUT["refund_paid"] = round(ref.refund_amount_paid.sum())
OUT["refund_paid_pct_of_gmv"] = round(100 * ref.refund_amount_paid.sum() / gmv, 2)
OUT["decisions"] = ref.refund_decision.value_counts().to_dict()
manual = ref[ref.refund_decision != "Auto-approved"]
auto = ref[ref.refund_decision == "Auto-approved"]
OUT["manual_share_pct"] = round(100 * len(manual) / len(ref))
OUT["decision_hours_manual_median"] = round(manual.decision_hours.median(), 1)
OUT["decision_hours_manual_p90"] = round(manual.decision_hours.quantile(.9), 1)
OUT["manual_over_24h_pct"] = round(100 * (manual.decision_hours > 24).mean())
OUT["chase_rate_manual_over_24h_pct"] = round(100 * (manual[manual.decision_hours > 24].chase_contacts > 0).mean())
OUT["chase_rate_manual_within_24h_pct"] = round(100 * (manual[manual.decision_hours <= 24].chase_contacts > 0).mean())
OUT["agent_hours_total"] = round(ref.agent_minutes.sum() / 60)
OUT["agent_cost_total"] = round(ref.agent_minutes.sum() / 60 * AGENT_COST_PER_HOUR)
OUT["manual_denial_rate_pct"] = round(100 * (manual.refund_decision == "Manual-denied").mean())
OUT["data_gap_missing_cancel_reason_pct"] = round(100 * canc.cancel_reason_code.isna().mean())

by_reason = ref.groupby("refund_reason").agg(cases=("order_id", "size"), requested=("refund_amount", "sum"), paid=("refund_amount_paid", "sum")).round(0).sort_values("paid", ascending=False)
by_reason["share_of_paid_pct"] = (100 * by_reason.paid / by_reason.paid.sum()).round(0)
by_reason.to_csv(A / "refunds_by_reason.csv")
OUT["by_reason"] = by_reason.reset_index().to_dict("records")

# lateness vs refund
deliv["late_min"] = deliv.actual_minutes - deliv.promised_minutes
deliv["late_bucket"] = pd.cut(deliv.late_min, [-100, 0, 10, 20, 40, 200], labels=["on time", "1-10 min late", "11-20", "21-40", ">40"])
late = deliv.groupby("late_bucket", observed=True).agg(orders=("order_id", "size"), refund_rate=("refund_requested", "mean")).round(3)
late.to_csv(A / "refund_rate_by_lateness.csv")
OUT["refund_rate_by_lateness"] = {k: round(100 * v, 1) for k, v in late.refund_rate.items()}
OUT["late_over_10_pct_of_delivered"] = round(100 * (deliv.late_min > 10).mean(), 1)

# serial refunders (concentration)
per_c = ref.groupby("customer_id").agg(cases=("order_id", "size"), paid=("refund_amount_paid", "sum"), requested=("refund_amount", "sum")).sort_values("requested", ascending=False)
n_c = d.customer_id.nunique()
top = per_c.head(int(np.ceil(0.05 * n_c)))
OUT["customers_total"] = n_c
OUT["customers_with_refund"] = len(per_c)
OUT["top5pct_customers"] = len(top)
OUT["top5pct_share_of_requests_pct"] = round(100 * top.cases.sum() / per_c.cases.sum())
OUT["top5pct_share_of_requested_value_pct"] = round(100 * top.requested.sum() / per_c.requested.sum())
OUT["customers_with_3plus_refunds"] = int((per_c.cases >= 3).sum())
per_c.head(20).to_csv(A / "top_refund_customers.csv")

# cancellations
cb = canc.groupby("cancelled_by").agg(cancellations=("order_id", "size"), wasted_food_cost=("wasted_food_cost", "sum")).round(0).sort_values("cancellations", ascending=False)
cs = canc.groupby(["cancelled_by", "cancel_stage"]).size().unstack(fill_value=0)
cb.to_csv(A / "cancellations_by_party.csv")
OUT["cancel_by"] = cb.reset_index().to_dict("records")
OUT["wasted_food_cost_total"] = round(canc.wasted_food_cost.sum())
OUT["cancel_after_food_prepared_pct"] = round(100 * canc.cancel_stage.isin(["During prep", "In transit"]).mean())
OUT["restaurant_stockout_pct_of_restaurant_cancels"] = round(100 * (canc[canc.cancelled_by == "Restaurant"].cancel_reason_code == "Item out of stock").mean())

# ---------------------------------------------------------------- what-if levers
# Lever 1: risk-based auto-approval. Raise the amount limit and keep the history rule.
rows = []
for limit, prior_max in ((10, 3), (15, 3), (15, 2), (20, 3), (20, 2)):    # (10, 3) is today's rule
    # cases moving to auto-approval = manual cases that the new rule would approve automatically
    flip = manual.iloc[0:0] if (limit, prior_max) == (10, 3) else \
        manual[(manual.refund_amount <= limit) & (manual.prior_refunds_90d < prior_max)]
    denied = flip[flip.refund_decision == "Manual-denied"]
    saved_min = flip.agent_minutes.sum() - 8 * len(flip)     # still pays the first-contact handling minutes
    chase_saved = flip.chase_contacts.sum()
    rows.append(dict(limit=limit, max_prior_refunds=prior_max - 1, cases_moved_to_auto=len(flip), pct_of_manual=round(100 * len(flip) / len(manual)),
                     refunds_that_manual_review_denied=len(denied), value_leaked_if_all_paid=round(denied.refund_amount.sum()),
                     agent_hours_saved=round(saved_min / 60, 1), agent_cost_saved=round(saved_min / 60 * AGENT_COST_PER_HOUR),
                     chase_contacts_avoided=int(chase_saved)))
lever1 = pd.DataFrame(rows)
lever1["net_benefit_if_leak_paid"] = lever1.agent_cost_saved - lever1.value_leaked_if_all_paid
lever1.to_csv(A / "whatif_lever1_auto_approval.csv", index=False)
OUT["lever1"] = lever1.to_dict("records")

# Lever 2: stop chasing: decision within 24h for manual cases (target) -> chase rate falls to the within-24h rate
over = manual[manual.decision_hours > 24]
within_rate = (manual[manual.decision_hours <= 24].chase_contacts > 0).mean()
chase_cost_per = 6 / 60 * AGENT_COST_PER_HOUR
exp_now = over.chase_contacts.sum()
exp_after = (over.chase_contacts > 0).sum() * 0 + len(over) * within_rate * over[over.chase_contacts > 0].chase_contacts.mean()
OUT["lever2"] = dict(manual_cases_over_24h=len(over), chase_contacts_now=int(exp_now), chase_contacts_if_within_24h=round(float(exp_after)),
                     agent_cost_saved=round(float((exp_now - exp_after) * chase_cost_per)))

# Lever 3: proactive credit for very late orders (>20 min late) that did not already get refunded
vl = deliv[deliv.late_min > 20]
vl_ref = vl[vl.refund_requested == 1]
cost_credit = PROACTIVE_CREDIT * len(vl)
refund_cases_late = vl_ref[vl_ref.refund_reason == "Late delivery"]
base_cost = refund_cases_late.refund_amount_paid.sum() + refund_cases_late.agent_minutes.sum() / 60 * AGENT_COST_PER_HOUR
rows = []
for name, avoided in (("conservative", .25), ("base", .50), ("optimistic", .75)):
    saved = base_cost * avoided
    rows.append(dict(scenario=name, share_of_late_refund_cases_avoided_pct=int(avoided * 100), cost_of_credits=round(cost_credit),
                     refund_and_handling_cost_avoided=round(saved), net=round(saved - cost_credit)))
lever3 = pd.DataFrame(rows)
lever3.to_csv(A / "whatif_lever3_proactive_credit.csv", index=False)
OUT["lever3"] = lever3.to_dict("records")
OUT["lever3_inputs"] = dict(very_late_orders=len(vl), late_refund_cases=len(refund_cases_late), current_cost=round(base_cost))

(A / "results.json").write_text(json.dumps(OUT, indent=2, default=str), encoding="utf-8")

# ---------------------------------------------------------------- figures
fig, ax = plt.subplots(1, 2, figsize=(11, 3.8))
by_reason.paid.sort_values().plot(kind="barh", ax=ax[0], color="#2f6f9f")
ax[0].set_title("Refund value paid by reason"); ax[0].set_ylabel(""); ax[0].set_xlabel("currency units")
late.refund_rate.mul(100).plot(kind="bar", ax=ax[1], color="#c0392b")
ax[1].set_title("Refund request rate by lateness"); ax[1].set_xlabel(""); ax[1].set_ylabel("% of delivered orders"); plt.setp(ax[1].get_xticklabels(), rotation=20)
plt.tight_layout(); plt.savefig(A / "figures" / "refunds_by_reason_and_lateness.png"); plt.close()

fig, ax = plt.subplots(figsize=(6, 3.8))
ax.hist(manual.decision_hours.clip(upper=72), bins=24, color="#2f6f9f")
ax.axvline(24, color="#c0392b", ls="--"); ax.text(25, ax.get_ylim()[1] * .9, "24 h", color="#c0392b")
ax.set_title(f"Manual refund decisions: hours to decide (auto-approved ≈ 0)"); ax.set_xlabel("hours (capped at 72)")
plt.tight_layout(); plt.savefig(A / "figures" / "manual_decision_time.png"); plt.close()

cum = per_c.requested.cumsum() / per_c.requested.sum()
fig, ax = plt.subplots(figsize=(6, 3.8))
ax.plot(np.arange(1, len(cum) + 1) / n_c * 100, cum * 100, color="#c0392b")
ax.axvline(5, color="grey", ls="--"); ax.set_xlabel("% of customers (ranked by refund value requested)"); ax.set_ylabel("% of refund value requested")
ax.set_title("Refund concentration"); plt.tight_layout(); plt.savefig(A / "figures" / "refund_concentration.png"); plt.close()

fig, ax = plt.subplots(figsize=(7, 3.8))
cs.plot(kind="bar", stacked=True, ax=ax, colormap="Set2"); ax.set_title("Cancellations by party and stage"); ax.set_xlabel(""); ax.set_ylabel("orders")
plt.xticks(rotation=0); plt.tight_layout(); plt.savefig(A / "figures" / "cancellations_by_party_and_stage.png"); plt.close()

print(json.dumps(OUT, indent=1, default=str))
