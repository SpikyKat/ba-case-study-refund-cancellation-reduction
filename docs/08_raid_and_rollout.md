# 8. RAID log and rollout plan

## Risks
| ID | Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|---|
| R1 | Higher limit invites refund abuse | Medium | High | Stricter history rule (at most 1 prior); weekly repeat-claimant list; guardrail alert at +0.2 pts; rollback in 1 hour | Risk |
| R2 | Agents distrust auto-approval or feel judged | Medium | Medium | Co-design workshops; show data; pilot feedback sessions; agents keep override on manual cases | Support |
| R3 | Tooling cannot support configurable rules or timers | Medium | High | Confirm in refinement before commitment; fall back to a manual daily queue report | Engineering |
| R4 | Pilot too small to show a result | High | Medium | Pilot in 3 cities, matched controls, about 95 cases per arm (see below) | BA |
| R5 | Cancellation reason becomes a "click anything" field | Medium | Medium | Short code list, mandatory stage, monthly data-quality check | Operations |
| R6 | Customers read the messages as a promise | Low | Medium | Legal-approved wording; "expected", not "guaranteed" | Legal |
| R7 | Metric definitions differ between teams | Medium | Medium | KPI definitions signed off by Data and Finance before the pilot | BA |

## Assumptions
A1 The support tool exposes refund history for 90 days. A2 Legal permits risk-based automation with an audit trail. A3 Agent cost is 20 per hour, and food loss on late cancellations is 60% of order value (see `assumptions_and_data.md`). A4 Customers' contact behaviour in the pilot matches the sample.

## Issues (open now)
I1 18% of historical cancellations lack a reason code, so root-cause history is incomplete. I2 No owner yet for the weekly repeat-claimant review.

## Dependencies
D1 Engineering capacity for rules engine and timers. D2 Product slot for the new refund form. D3 Legal review of customer messages. D4 Data/BI for the dashboard.

## Pilot design
- **Arms:** 3 pilot cities and 3 matched control cities (similar order volume and late-delivery rate). Compare the change in each arm over the same weeks (difference in differences), not a plain before/after, because seasonality and delivery performance move together. This is the lesson from the Service Operations case: a before/after change can be real but not provable.
- **Duration:** 4 weeks baseline and 8 weeks pilot.
- **Size:** detecting a fall in manual share from 60% to 40% needs about 95 refund cases per arm (80% power, 5% significance). At the sample's volume a city gets about 16 refund cases a month, so one city would take about six months; three cities take about two months.
- **Measures:** the KPIs in `07_kpis_and_benefits_case.md`, plus agent satisfaction survey and customer CSAT on refund contacts.

## Go / no-go criteria (proposed)
| Criterion | Go if |
|---|---|
| Guardrail | Refund value % of order value no more than 0.2 pts above control |
| Manual share | 45% or less in pilot cities |
| Decision time | Median 10 h or less |
| Defects | No open Critical or High |
| Agents | No majority "worse than before" in feedback |
| Legal and Risk | Both sign off |

If a criterion fails, extend the pilot or adjust limits; if the guardrail fails, roll back to the previous rules.

## Phases
| Phase | Weeks | Activities | Output |
|---|---|---|---|
| 0 Prepare | 1-3 | Interviews, KPI definitions, Legal review, tooling confirmation | Signed-off BRD |
| 1 Build and test | 4-8 | Configure rules and timers, form, messages; UAT (`06_uat_plan.md`) | UAT sign-off |
| 2 Pilot | 9-20 | Training, pilot in 3 cities, weekly KPI review | Pilot report |
| 3 Decide | 21 | Go / no-go with sponsor, Finance, Risk | Decision |
| 4 Scale | 22-26 | Roll out city by city, hypercare | BAU handover |

## Communications
| Audience | Message | Channel | When |
|---|---|---|---|
| Agents and leads | Why, what changes, what stays the same, how to give feedback | Team briefing and 30-minute training, job aid | 2 weeks before pilot |
| Finance and Risk | Guardrail, leak ceiling, rollback | Dashboard and weekly note | Weekly |
| Customers | Refund received, status at 4 h, outcome | In-app and email, Legal-approved wording | Live at pilot |
| Restaurants | Weekly stock-out summary (when built) | Partner portal | After pilot |

## Monitoring and rollback
Weekly KPI review during the pilot; daily check of the guardrail. Rollback restores the previous limits within one hour (NFR-6). Hypercare for four weeks after each scale step.
