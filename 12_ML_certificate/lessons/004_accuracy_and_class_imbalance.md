# Assignment 004 — Accuracy, baselines, and class imbalance

Module: 00, with introductory links to Modules 05 and 11. Suggested time: 15–20 minutes. Status: Complete; first submission correct.

## Lesson

Accuracy is the proportion of predictions that are correct:

`accuracy = correct predictions / total predictions × 100%`

A baseline is a simple reference approach to compare against. For classification, one baseline always predicts the most common class. It does not need a trained model, and it can have high accuracy if one class dominates.

Class imbalance means some outcome categories occur much more often than others. Example: of 200 historical subscribers, 180 stay and 20 cancel during the target month. An approach that always predicts "does not cancel" gets the 180 stayers right and the 20 cancellations wrong:

`accuracy = 180 / 200 × 100% = 90%`

Despite 90% accuracy, it identifies none of the actual cancellations. If the business needs to find customers at risk of leaving, this approach fails that goal. Accuracy is calculated correctly; it gives an incomplete picture of usefulness. We will next introduce a confusion matrix, precision, and recall to inspect which predictions are correct or missed.

## Your task — evaluate a simple baseline

In an evaluation dataset of 1,000 subscribers, 950 did not cancel during the target month and 50 canceled. A baseline predicts "does not cancel" for everyone.

1. How many predictions are correct, and what is the accuracy? Show the calculation.
2. How many of the 50 actual cancellations does it correctly identify as cancellations?
3. Is accuracy alone enough to decide whether this approach is useful for finding customers likely to cancel? Explain briefly.

Reply with answers 1–3. No coding or AWS resources needed. The historical outcomes are evaluation labels, not prediction inputs.

## Review criteria

Correct count and accuracy calculation; distinguish correct non-cancellation predictions from detected cancellations; explain why high accuracy can conceal failure on the minority class. Assignment remains incomplete until reviewed.

## Submission 1 — original wording (5 November 2026)

> 1. 950 are correct, 95%, 950 / 1000 * 100
> 2. 0
> 3. no, because this is only predict subscribers will stay, and not predict that subsciber will cancle. thats why.

## Review and completion

- All three answers correct: 950 correct predictions, 95% accuracy with the right calculation, and zero detected cancellations.
- Correct explanation that always predicting stay fails to identify cancellations, so accuracy alone cannot assess the intended business goal.
- Assignment 004 complete on first submission. Next: Assignment 005, confusion matrix, precision, and recall. Module 00 remains in progress.
