# 6. User acceptance test (UAT) plan

## Purpose and scope
Confirm that the changes in `04_requirements_BRD.md` work for the people who will use them, before the pilot. UAT covers the refund form, auto-approval rules, manual queue and timers, agent screen, customer messages, cancellation capture and the KPI dashboard.

## Roles
| Role | Responsibility |
|---|---|
| UAT lead (BA) | Plan, test data, triage defects, report |
| Testers | 2 team leads, 3 agents, 1 Risk analyst, 1 Finance analyst, 1 Product owner |
| Engineering | Fix defects, deploy builds to the test environment |
| Sponsor (Head of Support) | Final sign-off |

## Environment and data
Sandbox with the new rules enabled and fictional customers. Test data covers refund amounts of 5, 10, 12, 15, 16 and 40; customers with 0, 1, 2 and 3 prior refunds; each of the six reasons; late and on-time orders; cancellations by each of the four parties.

## Entry criteria
Build deployed to sandbox; test data loaded; requirement list frozen; testers trained for 30 minutes.

## Exit criteria
All Must test cases pass; no open Critical or High defects; Medium defects have an agreed owner and date; sign-off by the sponsor, Finance and Risk.

## Defect severity
| Severity | Meaning | Example |
|---|---|---|
| Critical | Money or customer data at risk, or process blocked | Refund above limit auto-approved |
| High | Core function wrong, with no workaround | Overdue alert never sent |
| Medium | Function wrong, with a workaround | Wrong sort order in queue |
| Low | Cosmetic | Typo in message |

## Test cases
| ID | Req | Scenario | Steps | Expected result | Priority |
|---|---|---|---|---|---|
| T-01 | FR-1 | Reason required | Open form, submit with no reason | Blocked with message | Must |
| T-02 | FR-2 | Item picker | Choose "missing item" | Order items shown; at least one required | Must |
| T-03 | FR-3 | Auto-approve inside limits | Amount 12, 0 prior refunds | Approved within 5 s | Must |
| T-04 | FR-3 | Amount just above limit | Amount 16, 0 prior refunds | Goes to manual queue | Must |
| T-05 | FR-3 | History at maximum | Amount 12, 2 prior refunds | Goes to manual queue | Must |
| T-06 | FR-3 | Amount at limit | Amount 15, 1 prior refund | Approved automatically | Must |
| T-07 | FR-4 | Admin changes limit | Authorised admin sets limit 12; submit 14 | Manual; change logged with user and time | Must |
| T-08 | FR-4 | Unauthorised change | Agent tries to change limit | Denied; attempt logged | Must |
| T-09 | FR-5 | Queue timer | Create manual case | Shows 8 h target | Must |
| T-10 | FR-6 | Overdue alert | Advance case past 8 h | Lead alerted; case marked overdue | Must |
| T-11 | FR-6 | Queue order | Create 3 cases of different age and value | Oldest and highest value first | Should |
| T-12 | FR-7 | Agent screen | Open a case | Items, amount, lateness, 90-day history, flags shown | Must |
| T-13 | FR-9 | Decision needs reason | Try to close without reason code | Blocked | Must |
| T-14 | FR-8 | Receipt message | Submit request | Message within 1 minute | Must |
| T-15 | FR-8 | 4-hour message | Leave undecided past 4 h | Status message sent once | Must |
| T-16 | NFR-4 | Denial message | Deny a case | Plain-language reason, approved wording | Must |
| T-17 | FR-10 | Repeat list | Create customer with 3 requests in 90 days | Appears in weekly list | Should |
| T-18 | FR-11 | Mandatory cancel reason | Cancel an order with no reason | Blocked until reason and stage given | Must |
| T-19 | FR-11 | System cancellation | Payment-failed cancellation | Reason filled automatically | Must |
| T-20 | RR-1 | Dashboard values | Load known test data | KPIs equal hand-calculated values | Must |
| T-21 | RR-2 | Guardrail alert | Load data with refund value +0.3 pts | Alert to Finance and Support | Must |
| T-22 | NFR-6 | Rollback | Revert rules to previous version | Previous limits active within 1 hour | Must |
| T-23 | NFR-2 | Audit trail | Review a decision and a rule change | Who, when, what recorded | Must |

## Reporting and sign-off
Daily pass/fail summary during UAT; a final report listing results by requirement, open defects and a recommendation. Sign-off form lists the three signatories and any accepted risks.
