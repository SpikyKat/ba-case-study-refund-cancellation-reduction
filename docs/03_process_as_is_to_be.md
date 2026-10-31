# 3. Process: as-is and to-be

Diagrams are Mermaid (render on GitHub).

## As-is: refund request
```mermaid
flowchart TD
    A[Customer reports a problem in app or by phone] --> B[Free-text reason, no structure]
    B --> C[Agent finds the order and checks history in several screens]
    C --> D{Amount 10 or less AND fewer than 3 refunds in 90 days?}
    D -- Yes --> E[Auto-approved, about 0 h]
    D -- No --> F[Manual queue, no timer, no priority]
    F --> G[Agent review, median 14.5 h, p90 40 h]
    G --> H{Approve?}
    H -- Yes --> I[Refund paid]
    H -- No --> J[Denied, customer told]
    F -. no status update .-> K[Customer chases, 51% if decision over 24 h]
    K --> F
```

### Pain points (with evidence)
| # | Pain point | Evidence |
|---|---|---|
| P1 | 60% of refund cases go to manual review | 375 of 623 cases |
| P2 | Slow decisions with no timer | Median 14.5 h; 23% over 24 h |
| P3 | Customers chase because there is no status | 51% chase when over 24 h vs 17% under |
| P4 | Reason is free text, so it cannot be analysed reliably | Reasons must be inferred |
| P5 | Repeat claimants are found only by manual lookup | 42 customers with 3 or more refunds |
| P6 | Cancellation reason and stage are not enforced | 18% of cancellations have no reason |

## To-be: refund request
```mermaid
flowchart TD
    A[Customer starts refund in app] --> B[Structured reason + order item picker + photo for missing items]
    B --> C[Rules engine scores the case: amount, reason, history, lateness]
    C --> D{Low risk: amount 15 or less AND at most 1 refund in 90 days?}
    D -- Yes --> E[Auto-approved, customer told in minutes]
    D -- No --> F[Manual queue with priority and 8 h timer]
    F --> G[Agent sees order, history and risk flags on one screen]
    G --> H{Decision}
    H -- Approve --> I[Refund paid]
    H -- Deny --> J[Denied with a reason code and plain-language message]
    F --> K[Status message at receipt and at 4 h]
    F --> L[Timer breach alerts the team lead]
    I --> M[Weekly repeat-refund review list to Risk]
    J --> M
```

### What changes
| Area | As-is | To-be | Addresses |
|---|---|---|---|
| Intake | Free text | Structured reason, item picker, photo for missing items | P4 |
| Auto-approval | 10 limit, fewer than 3 refunds | 15 limit, at most 1 prior refund (pilot) | P1 |
| Queue | No timer or priority | 8 h target, priority by age and value, lead alert | P2 |
| Customer communication | Silence | Receipt and 4 h status messages | P3 |
| Risk monitoring | Manual lookup | Weekly repeat-refund list | P5 |

## As-is and to-be: cancellations
```mermaid
flowchart LR
    A[Order cancelled] --> B{Reason and stage captured?}
    B -- "As-is: optional, 18% blank" --> C[Reasons unreliable]
    B -- "To-be: mandatory code + stage" --> D[Weekly view by party, stage, restaurant]
    D --> E[Stock-out alerts to restaurant partners]
```
Cancellations after food is prepared or on the way (68% of cancellations) are the costly ones. The to-be process makes them visible so partnerships and operations can act on them; this case does not model a savings figure for that.
