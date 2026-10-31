# 2. Stakeholders and elicitation plan

> Fictional. The needs listed are hypotheses drawn from the baseline data and common practice; the interview plan is how I would test them.

## Stakeholder map
| Stakeholder | Interest | Influence | Main concern (hypothesis) | Engagement |
|---|---|---|---|---|
| Head of Customer Support (sponsor) | Cost per contact, customer satisfaction | High | Faster decisions without losing control | Weekly sponsor update |
| Support team leads | Queue health, agent workload | High | Rules they cannot explain to customers | Co-design workshops |
| Support agents | Daily workflow | Medium | More auto-approvals means less judgement, or more blame | Pilot feedback sessions |
| Finance | Refund cost, leakage | High | Any rise in refund value | Guardrail sign-off |
| Risk / Fraud | Abuse of refunds | High | Looser limits being exploited | Rule design and monitoring |
| Product (consumer app) | Intake form, notifications | High | Delivery time and UI effort | Requirements review |
| Engineering (support tooling) | Rules engine, timers, events | High | Effort, data model | Refinement sessions |
| Restaurant partnerships | Cancellations, stock-outs | Medium | Penalties for partners | Impact consultation |
| Legal / Compliance | Consumer rights, data use | High (veto) | Fair treatment, transparency | Policy review before pilot |
| Data / BI | Reporting, metric definitions | Medium | Consistent definitions | KPI definition workshop |
| Customers | Quick fair resolution | n/a | Clear status and outcome | Survey and usability test |

## RACI (summary)
| Activity | Support | Finance | Risk | Product | Engineering | Legal | BA |
|---|---|---|---|---|---|---|---|
| Approve auto-approval limits | A | C | R | I | I | C | C |
| Define requirements | C | C | C | C | C | I | R/A |
| Build rules and timers | I | I | C | C | R/A | I | C |
| Cancellation reason capture | C | I | I | R | R | I | A |
| UAT | A | I | C | R | C | I | R |
| Go / no-go | A | C | C | C | C | C | R (prepares) |

R = responsible, A = accountable, C = consulted, I = informed.

## Elicitation plan
1. **Data review (done):** baseline analysis in `09_baseline_analysis.md`.
2. **Interviews (30 min each):** sponsor, two team leads, three agents, Finance, Risk, Product. Questions: "Walk me through the last refund you decided. What did you check? What made you escalate? Which decisions do you feel are low risk? What do customers say when they chase?"
3. **Observation:** shadow agents on 20 refund cases to log systems opened and minutes spent.
4. **Workshop:** rule design with Support, Risk and Finance: choose the auto-approval limit and history rule with the data in hand.
5. **Document analysis:** current refund policy, macros, QA scorecard, consumer-rights requirements.
6. **Prototype review:** show the to-be intake and status messages to Product and five agents.

## Conflicting needs and how I would handle them
- **Support wants speed; Risk wants control.** Use the data: raising the limit to 15 with a stricter history rule moves 33% of manual cases to auto, and at most 19 of 122 (16%) would have been denied by manual review. Agree a guardrail and a pilot.
- **Product wants a simple form; Finance wants evidence.** Ask for evidence only where it helps (photo for missing items), not on every case.
