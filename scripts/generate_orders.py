"""Fake order and refund data for the Plateful refunds case. All invented, see docs/assumptions_and_data.md.

usage: python scripts/generate_orders.py --n 10000 --seed 11
"""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
CITIES = {"London": .30, "Manchester": .15, "Birmingham": .12, "Dublin": .15, "Madrid": .18, "Barcelona": .10}
CITY_DELAY = {"London": 0, "Manchester": 1, "Birmingham": 5, "Dublin": 0, "Madrid": 3, "Barcelona": 2}
HOUR_W = {10: 1, 11: 3, 12: 8, 13: 8, 14: 4, 15: 2, 16: 2, 17: 4, 18: 8, 19: 10, 20: 8, 21: 4, 22: 2}
DAY_W = [.9, .9, .95, 1, 1.25, 1.35, 1.1]   # Mon..Sun
AUTO_LIMIT, AUTO_PRIOR_MAX = 10.0, 3          # current policy: auto-approve if amount <= 10 and < 3 refunds in 90 days
FOOD_LOSS_SHARE = 0.60                        # assumption: share of order value lost if cancelled after food is prepared


def pick(rng, mapping):
    k = list(mapping)
    p = np.array([mapping[x] for x in k], float)
    return k[rng.choice(len(k), p=p / p.sum())]


def generate(n, seed):
    rng = np.random.default_rng(seed)
    days = pd.date_range("2025-01-01", "2025-06-30")
    dw = np.array([DAY_W[d.weekday()] for d in days])
    n_cust = 900
    abusers = set(rng.choice(n_cust, size=36, replace=False))          # hidden truth, not in the output
    cw = np.array([3.0 if c in abusers else 1.0 for c in range(n_cust)])
    cw /= cw.sum()
    hours, hw = list(HOUR_W), np.array(list(HOUR_W.values()), float)
    rows = []
    for _ in range(n):
        d = days[rng.choice(len(days), p=dw / dw.sum())]
        h = int(rng.choice(hours, p=hw / hw.sum()))
        created = d + pd.Timedelta(hours=h, minutes=int(rng.integers(60)), seconds=int(rng.integers(60)))
        city = pick(rng, CITIES)
        cust = int(rng.choice(n_cust, p=cw))
        value = float(np.clip(rng.lognormal(np.log(22), 0.45), 8, 120))
        if cust in abusers:
            value *= 1.25
        promised = int(rng.choice([25, 30, 35, 40, 45]))
        peak = 7 if (d.weekday() >= 4 and 18 <= h <= 21) else 0
        delay = rng.normal(-2, 8) + peak + CITY_DELAY[city] + (rng.random() < 0.08) * rng.uniform(15, 35)
        rows.append(dict(created_at=created, city=city, customer_id=f"C{cust:04d}", restaurant_id=f"R{int(rng.integers(1, 61)):03d}",
                         items=int(rng.integers(1, 7)), order_value=round(value, 2), promised_minutes=promised,
                         hid_delay=delay, hid_abuser=cust in abusers))
    df = pd.DataFrame(rows).sort_values("created_at").reset_index(drop=True)
    df.insert(0, "order_id", [f"O{i + 1:05d}" for i in range(len(df))])

    out = []
    for r in df.itertuples():
        rec = dict(status="Delivered", cancelled_by=None, cancel_stage=None, cancel_reason_code=None, wasted_food_cost=0.0,
                   actual_minutes=None, refund_requested=0, refund_reason=None, refund_amount=0.0)
        p_cancel = 0.07 + 0.10 * (r.hid_delay > 20)
        if rng.random() < p_cancel:
            who = pick(rng, {"Customer": .45 + (.15 if r.hid_delay > 20 else 0), "Restaurant": .30, "Courier": .15, "System": .10})
            stage = {"Customer": pick(rng, {"Before acceptance": .3, "During prep": .4, "In transit": .3}),
                     "Restaurant": pick(rng, {"During prep": .7, "After acceptance": .3}),
                     "Courier": "In transit",
                     "System": pick(rng, {"Before acceptance": .6, "After acceptance": .4})}[who]
            reasons = {"Customer": ["Changed mind", "Took too long", "Wrong address", "Ordered by mistake"],
                       "Restaurant": ["Item out of stock", "Kitchen too busy", "Restaurant closed"],
                       "Courier": ["Vehicle problem", "Could not find address", "Unavailable"],
                       "System": ["Payment failed", "Duplicate order", "Fraud check"]}[who]
            rec.update(status="Cancelled", cancelled_by=who, cancel_stage=stage,
                       cancel_reason_code=None if rng.random() < 0.20 else reasons[int(rng.integers(len(reasons)))],
                       wasted_food_cost=round(FOOD_LOSS_SHARE * r.order_value, 2) if stage in ("During prep", "In transit") else 0.0)
        else:
            actual = max(12, r.promised_minutes + r.hid_delay)
            rec["actual_minutes"] = round(actual, 0)
            late = actual > r.promised_minutes + 10
            if r.hid_abuser:
                p_req = 0.25
                reason = pick(rng, {"Missing item": .45, "Never arrived": .40, "Wrong item": .15})
            elif late:
                p_req = 0.18
                reason = pick(rng, {"Late delivery": .70, "Quality": .15, "Missing item": .15})
            else:
                p_req = 0.015
                reason = pick(rng, {"Missing item": .35, "Quality": .30, "Wrong item": .15, "Never arrived": .08, "Other": .12})
            if rng.random() < p_req:
                amt = {"Late delivery": 0.5, "Never arrived": 1.0}.get(reason) or {"Missing item": rng.uniform(.15, .4), "Wrong item": rng.uniform(.5, 1), "Quality": rng.uniform(.3, .6), "Other": rng.uniform(.1, .5)}[reason]
                rec.update(refund_requested=1, refund_reason=reason, refund_amount=round(float(amt) * r.order_value, 2))
        out.append(rec)
    df = pd.concat([df, pd.DataFrame(out)], axis=1)

    # refund decisions, in time order so "refunds in the previous 90 days" is known when a case arrives
    df["prior_refunds_90d"] = 0
    df["refund_decision"] = None
    df["decision_hours"] = np.nan
    df["agent_minutes"] = 0.0
    df["contact_channel"] = None
    df["chase_contacts"] = 0
    history = {}
    for i, r in df.iterrows():
        if not r.refund_requested:
            continue
        past = [t for t in history.get(r.customer_id, []) if t > r.created_at - pd.Timedelta(days=90)]
        df.at[i, "prior_refunds_90d"] = len(past)
        history.setdefault(r.customer_id, []).append(r.created_at)
        chan = pick(rng, {"App chat": .60, "Phone": .25, "Email": .15})
        df.at[i, "contact_channel"] = chan
        handle = {"App chat": 8, "Phone": 12, "Email": 10}[chan]
        if r.refund_amount <= AUTO_LIMIT and len(past) < AUTO_PRIOR_MAX:
            df.at[i, "refund_decision"] = "Auto-approved"
            df.at[i, "decision_hours"] = 0.05
            df.at[i, "agent_minutes"] = 0.0
        else:
            deny = (0.55 if r.hid_abuser else 0.12) + (0.15 if len(past) >= 3 else 0.0)
            df.at[i, "refund_decision"] = "Manual-denied" if rng.random() < deny else "Manual-approved"
            hrs = float(rng.lognormal(np.log(14), 0.8))
            df.at[i, "decision_hours"] = round(hrs, 1)
            df.at[i, "agent_minutes"] = round(float(rng.lognormal(np.log(12), 0.4)), 1)
            if rng.random() < (0.5 if hrs > 24 else 0.15):
                df.at[i, "chase_contacts"] = int(rng.integers(1, 4))
        df.at[i, "agent_minutes"] += handle + 6 * df.at[i, "chase_contacts"]
    df.loc[df.refund_decision == "Manual-denied", "refund_amount_paid"] = 0.0
    df["refund_amount_paid"] = np.where(df.refund_decision.isin(["Auto-approved", "Manual-approved"]), df.refund_amount, 0.0)
    return df.drop(columns=["hid_delay", "hid_abuser"])


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=10000)
    ap.add_argument("--seed", type=int, default=11)
    a = ap.parse_args()
    d = generate(a.n, a.seed)
    out = ROOT / "data"
    out.mkdir(exist_ok=True)
    d.to_csv(out / "orders.csv", index=False, lineterminator="\n", date_format="%Y-%m-%d %H:%M:%S")
    print(f"orders.csv: {len(d)} rows; delivered {int((d.status == 'Delivered').sum())}, cancelled {int((d.status == 'Cancelled').sum())}, refund cases {int(d.refund_requested.sum())}")
