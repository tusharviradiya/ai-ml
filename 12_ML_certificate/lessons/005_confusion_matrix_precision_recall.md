# Assignment 005 — Confusion matrix, precision, and recall

Module: 00, introducing Module 11 evaluation concepts. Suggested time: 20–25 minutes. Status: Complete after correction; historical task and reviews preserved below.

## Lesson

Choose a positive class before calculating these metrics. Here positive means "cancels during the target month" and negative means "does not cancel during that month." Positive names the outcome of interest; it does not mean desirable.

Evaluate predictions against known historical outcomes. The four counts form a confusion matrix:

| | Actually cancels | Actually stays |
|---|---|---|
| Predicts cancellation | True positive (TP): correctly flags cancellation | False positive (FP): false alarm |
| Predicts stay | False negative (FN): misses cancellation | True negative (TN): correctly predicts stay |

Precision asks: Of everyone flagged as likely to cancel, how many actually canceled?

`precision = TP / (TP + FP)`

Recall asks: Of everyone who actually canceled, how many did we flag?

`recall = TP / (TP + FN)`

Multiply the fractions by 100 to express percentages. Accuracy remains `(TP + TN) / total`.

Worked example: flag 10 subscribers; 8 actually cancel and 2 stay. Another 4 cancellations are missed. Then TP = 8, FP = 2, FN = 4. Precision is 8/10 = 80%; recall is 8/12 ≈ 66.7%. Precision counts correct flags among flags; recall counts detected cancellations among actual cancellations.

Higher precision reduces the fraction of false alarms among flagged cases. Higher recall reduces the fraction of actual cancellations missed. Which matters more depends on the goal and consequences of errors; neither alone fully describes model quality. Threshold tradeoffs come later. If a denominator is zero, the fraction is undefined mathematically and tools use documented handling; no such case occurs in this exercise.

## Your task — one evaluation scenario

For 100 subscribers:

- 30 are predicted to cancel: 20 actually cancel and 10 stay.
- 70 are predicted to stay: 5 actually cancel and 65 stay.

1. Give TP, FP, FN, and TN, with a short description of what FP and FN mean here.
2. Calculate precision. Show the numerator and denominator; round to one decimal place if needed.
3. Calculate recall. Show the numerator and denominator.

Reply with answers 1–3. No coding or AWS resources needed. Completion requires reviewed evidence of outcome mapping and both denominators.

## Submission 1 — original wording (5 November 2026)

> 1. its all about what we predict, and what is actual, based on that we tell this TP, FP, FN and TN. false positives means our model predict that customer will cancle, but actually user will stay, and false negatives means we predict that user will stay but actually user will cancle plan.
> 2. precision = 20/(20+5) = 20/25
> 3. recall = 20/(20+10) = 20/30

## Review 1

- Correctly explains predicted versus actual outcomes and the meanings of FP and FN. Requested numerical counts were omitted.
- Counts are TP = 20, FP = 10, FN = 5, TN = 65.
- Precision and recall were swapped. The submitted 20/25 is recall; 20/30 is precision. Percentages were not supplied.
- Precision looks at predicted positives: 30 flagged, of whom 20 actually canceled. Precision = 20/(20+10) ≈ 66.7%.
- Recall looks at actual positives: 25 canceled, of whom 20 were flagged. Recall = 20/(20+5) = 80%.
- Reinforcement: precision asks whether cancellation predictions are reliable; recall asks how many actual cancellations were caught. Work out the denominator in words before inserting numbers.

## Current task — targeted transfer check

A new evaluation gives TP = 12, FP = 3, FN = 8, TN = 77.

1. Calculate precision and recall as percentages. For each, explain who is included in its denominator.
2. Which count represents missed cancellations: FP or FN?

Reply with answers 1–2. Assignment remains active; overall completed count remains 4.

## Submission 2 — original wording (5 November 2026)

> 1. precision = 12/(12+3) = 80%, recall = 12/(12+8) = 60%, precision  includes false positive (predict : will cancle, but actual : stay), recall includes false nagetive (predict : stay and actual : cancale)
> 2. FN.

## Review and completion

- Both calculations correct: precision = 80%, recall = 60%.
- Correctly associates FP with precision and FN with recall, with accurate descriptions. FN correctly identifies missed cancellations.
- Reinforced whole denominator populations: precision includes all 15 predicted cancellations (12 TP + 3 FP), recall includes all 20 actual cancellations (12 TP + 8 FN), rather than errors alone.
- Assignment 005 complete after correction; overall completed count is 5. Next: decision thresholds and their effects on precision/recall. Module 00 remains in progress.
