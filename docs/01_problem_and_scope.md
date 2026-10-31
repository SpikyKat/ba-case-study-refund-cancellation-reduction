# 1. Problem statement and scope

> Fictional case study. Plateful is an invented food-delivery marketplace; all data is synthetic (see `assumptions_and_data.md`). Stakeholder needs below are assumptions I would validate in interviews.

## Business context
Plateful's customers can ask for a refund when an order is late, incomplete or never arrives, and orders can be cancelled by the customer, restaurant, courier or system. Refund requests go to support, which approves small cases automatically and sends everything else to a manual review queue.

## Problem
Over six months (10,000 sample orders), refunds and cancellations cost money and agent time, and slow decisions generate repeat contacts:
- **Refund requests:** 623 on 9,216 delivered orders (6.8%). Refunds paid were 2.28% of order value.
- **Manual review is the default:** 60% of refund cases go to manual review (375 of 623). The median decision takes 14.5 hours; 23% take more than 24 hours.
- **Slow decisions create chasing:** when a manual decision takes over 24 hours, 51% of customers contact support again, against 17% when it takes under 24 hours.
- **Cancellations waste food:** 784 orders were cancelled (7.8%). 68% were cancelled after food was being prepared or was on the way. Under an assumed 60% food loss, that is about 8,100 currency units wasted.
- **Poor data:** 18% of cancellations have no reason code, so the business cannot see why orders are cancelled.
- **Refund abuse:** the 45 customers with the most refund value (5% of customers) account for 56% of the value requested.

## Objectives (SMART, proposed)
| # | Objective | Baseline | Proposed target | By |
|---|---|---|---|---|
| O1 | Cut the share of refund cases needing manual review | 60% | 40% or less | End of pilot + 8 weeks |
| O2 | Speed up manual decisions | median 14.5 h; 23% over 24 h | median 8 h or less; under 5% over 24 h | End of pilot + 8 weeks |
| O3 | Reduce repeat contacts from waiting customers | 51% chase rate on >24 h cases | under 20% | End of pilot + 8 weeks |
| O4 | Keep refund cost under control | 2.28% of order value | no more than 0.2 points above baseline (at most 2.48%); worst case modelled at 2.37% | Ongoing |
| O5 | Make cancellation reasons visible | 18% missing | under 2% | Pilot start |

Targets are proposals for the business to confirm, not forecasts.

## Scope
**In scope:** refund intake and decision flow, risk-based auto-approval rules, manual queue handling and timers, customer status messages, cancellation reason and stage capture, repeat-refund monitoring, reporting.
**Out of scope:** changing delivery operations or courier allocation, payment-provider chargebacks, legal policy changes, a full fraud-detection model.

## Constraints and assumptions
- Customer-facing policy changes need Legal and Customer Support leadership approval.
- The support tool supports configurable rules and queue timers (to be confirmed with Engineering).
- Agent cost is assumed at 20 currency units per hour fully loaded; food loss on late cancellations at 60% of order value.
- Proactive credits were tested and rejected on cost (see `07_kpis_and_benefits_case.md`).
