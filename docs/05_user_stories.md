# 5. User stories and acceptance criteria

Format: As a ... I want ... so that ... Acceptance criteria are Given / When / Then. Priority follows `04_requirements_BRD.md`.

## US-1 Structured refund request (FR-1, FR-2) Must
As a customer, I want to pick what went wrong and which items were affected, so that my request is understood without back-and-forth.
- Given an order delivered in the last 7 days, when I open the refund form, then I see the six reasons as options and cannot submit without choosing one.
- Given I choose "missing item", when I continue, then I see my order's items and must select at least one.
- Given I choose "missing item" or "wrong item", when I continue, then I can attach one photo, and it is optional.
- Given I submit, when the request is saved, then I see a confirmation and a reference number.

## US-2 Auto-approve low-risk refunds (FR-3, FR-4) Must
As a support team lead, I want low-risk refunds approved automatically, so that agents spend time on the cases that need judgement.
- Given a refund of 12 from a customer with 0 refunds in 90 days, when the limit is 15 and the history maximum is 1, then it is approved automatically within 5 seconds.
- Given a refund of 12 from a customer with 2 refunds in 90 days, when it is submitted, then it goes to the manual queue.
- Given I am an authorised administrator, when I change the limit, then the change applies to new requests only and is logged with my name and the time.
- Given a refund above the limit, when it is submitted, then it is never auto-approved.

## US-3 Queue timer and priority (FR-5, FR-6) Must
As a team lead, I want manual cases sorted and timed, so that nothing waits unseen.
- Given a case enters the queue, when it is created, then it shows a target decision time of 8 hours.
- Given a case passes 8 hours undecided, when the timer expires, then I receive an alert and the case is marked overdue.
- Given the queue has cases of different ages, when an agent opens it, then the oldest and highest-value cases appear first.

## US-4 One-screen decision (FR-7, FR-9) Must
As an agent, I want the order, history and risk flags on one screen, so that I can decide without switching tools.
- Given I open a case, when the screen loads, then I see items, amount, delivery lateness, and refund history for the last 90 days.
- Given the customer has 3 or more refund requests in 90 days, when I open the case, then a "repeat claimant" flag is shown.
- Given I decide, when I save, then I must choose an outcome and a reason code before the case closes.

## US-5 Status messages (FR-8) Must
As a customer, I want to know my request was received and what is happening, so that I do not need to contact support again.
- Given I submit a refund request, when it is saved, then I receive a message within 1 minute confirming receipt and the expected time.
- Given my request is still undecided at 4 hours, when the 4-hour mark passes, then I receive a status message.
- Given a decision is made, when it is saved, then I receive the outcome and, if denied, the reason in plain language.

## US-6 Repeat-refund review list (FR-10) Should
As a risk analyst, I want a weekly list of repeat claimants, so that I can review patterns without searching case by case.
- Given the week has ended, when the report runs, then it lists customers with 3 or more requests in 90 days with count, value, reasons and decisions.
- Given I open the list, when I select a customer, then I can see their cases but not payment details.

## US-7 Mandatory cancellation reason (FR-11) Must
As an operations analyst, I want every cancellation to have a reason and stage, so that I can see why orders fail.
- Given a cancellation is recorded by any party, when the record is saved, then reason code and stage are required.
- Given an automated system cancellation, when it is recorded, then a system reason is filled automatically.
- Given a cancellation is missing either field, when a user tries to close it, then the system blocks closing and says what is missing.

## US-8 Stock-out summary (FR-12) Could
As a restaurant partnerships manager, I want a weekly summary of stock-out cancellations by restaurant, so that I can discuss availability with them.
- Given the week has ended, when the report runs, then it lists restaurants by number of "item out of stock" cancellations.

## US-9 Late-order notification (FR-13) Could
As a customer, I want to be told early when my order will be late, so that I can decide whether to wait.
- Given an order's estimated arrival is more than 10 minutes later than promised, when this is detected, then I receive a message with the new time.
- Given the order is on time, when it is delivered, then no late message is sent.

## US-10 KPI dashboard (RR-1, RR-2) Must
As the head of support, I want one weekly dashboard of the agreed KPIs, so that I can see whether the change is working and safe.
- Given the week has ended, when the dashboard refreshes, then it shows manual share, median and p90 decision time, share over 24 hours, chase rate, refund value as % of order value, and missing cancellation reasons.
- Given refund value as % of order value is more than 0.2 percentage points above baseline, when the dashboard refreshes, then an alert is sent to Finance and Support.
