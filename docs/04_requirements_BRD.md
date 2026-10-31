# 4. Business requirements document (BRD)

Priority uses MoSCoW (Must, Should, Could, Won't now). Each requirement traces to a finding, an objective and a user story (US) in `05_user_stories.md`.

## Business requirements
| ID | Requirement | Objective | Priority |
|---|---|---|---|
| BR-1 | Reduce manual review of low-risk refund cases without raising refund cost | O1, O4 | Must |
| BR-2 | Decide manual cases faster and make the wait visible | O2, O3 | Must |
| BR-3 | Make cancellation reasons and stages reliable | O5 | Must |
| BR-4 | Detect repeat refund claimants early | O4 | Should |
| BR-5 | Report the KPIs weekly with consistent definitions | all | Must |

## Functional requirements
| ID | Requirement | Source finding | Story | Priority |
|---|---|---|---|---|
| FR-1 | The refund form shall capture a structured reason (late delivery, missing item, wrong item, quality, never arrived, other) | P4 | US-1 | Must |
| FR-2 | For "missing item" or "wrong item", the customer shall pick the affected items and may attach a photo | P4 | US-1 | Should |
| FR-3 | The system shall auto-approve a refund when the amount is at most the configured limit (pilot: 15) and prior refunds in 90 days are at most the configured maximum (pilot: 1) | P1 | US-2 | Must |
| FR-4 | Auto-approval limit and history rule shall be configurable by an authorised Support administrator without a code release | P1 | US-2 | Must |
| FR-5 | Cases not auto-approved shall enter a manual queue with a timer (target 8 h) | P2 | US-3 | Must |
| FR-6 | The queue shall be sorted by age and value, and overdue cases shall alert the team lead | P2 | US-3 | Must |
| FR-7 | The agent screen shall show order details, customer refund history (90 days) and risk flags together | P2, P5 | US-4 | Must |
| FR-8 | The customer shall receive a message when the request is received and again if undecided at 4 h | P3 | US-5 | Must |
| FR-9 | Every manual decision shall record an outcome and reason code (including denial reasons) | P2 | US-4 | Must |
| FR-10 | The system shall produce a weekly list of customers with 3 or more refund requests in 90 days for Risk review | P5 | US-6 | Should |
| FR-11 | Cancellation shall require a reason code and a stage; the order cannot be closed without them | P6 | US-7 | Must |
| FR-12 | Restaurant cancellations for "item out of stock" shall be summarised weekly by restaurant | P6 | US-8 | Could |
| FR-13 | The system shall notify the customer proactively when an order is more than 10 minutes late (message only, no credit) | P3 | US-9 | Could |

## Non-functional requirements
| ID | Requirement | Priority |
|---|---|---|
| NFR-1 | Auto-approval decisions complete in under 5 seconds | Must |
| NFR-2 | Every rule change and every decision is logged with who, when, and what changed (audit trail) | Must |
| NFR-3 | Customer data is handled under the company's data-protection policy; refund history is visible only to support and risk roles | Must |
| NFR-4 | Messages and denial reasons use plain language and comply with consumer-rights wording approved by Legal | Must |
| NFR-5 | The new intake form meets the same accessibility standard as the rest of the app | Should |
| NFR-6 | The rules can be rolled back to the previous configuration within one hour | Must |

## Data and reporting requirements
| ID | Requirement | Priority |
|---|---|---|
| DR-1 | Refund and cancellation events carry order ID, customer ID, reason code, amount, decision, decision time, agent minutes | Must |
| DR-2 | A pilot flag identifies cases handled under the new rules (to compare with the control city) | Must |
| RR-1 | Weekly dashboard: manual share, median and p90 decision time, share over 24 h, chase rate, refund value as % of order value, missing cancellation reasons | Must |
| RR-2 | Guardrail alert if refund value as % of order value rises more than 0.2 percentage points above baseline | Must |

## Out of scope (Won't now)
Machine-learning fraud scoring; changes to courier allocation; automatic payment-provider dispute handling.

## Business rules
- BRL-1: A refund is never higher than the order value.
- BRL-2: A denied refund always gets a reason code and a customer message.
- BRL-3: Limits and history rules apply per customer, not per order.

## Traceability (objective to requirements)
| Objective | Requirements |
|---|---|
| O1 manual share | FR-1, FR-3, FR-4 |
| O2 decision speed | FR-5, FR-6, FR-7, FR-9 |
| O3 chasing | FR-8, FR-13 |
| O4 refund cost guardrail | FR-3, FR-10, RR-2 |
| O5 cancellation reasons | FR-11, FR-12 |

## Open questions
1. Does the support tool allow configurable rules and queue timers, or does this need development?
2. Which reason codes does Legal require customers to see on a denial?
3. Who owns the weekly repeat-refund review in Risk?
