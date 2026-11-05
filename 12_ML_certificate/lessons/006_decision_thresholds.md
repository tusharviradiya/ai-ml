# Assignment 006 — Decision thresholds

Module: 00, introducing Module 11 evaluation concepts. Suggested time: 20–25 minutes. Status: Assigned; awaiting submission.

## Lesson

A binary classifier can output a score for cancellation, often presented as an estimated probability between 0 and 1. A decision threshold converts the score into a label. In this lesson, predict cancellation when score >= threshold; otherwise predict stay. Scores are estimates, not guarantees; probability calibration is a later topic.

At threshold 0.5, a score of 0.7 is flagged and 0.4 is not. Lowering the threshold to 0.3 flags both. This changes the decisions without retraining or changing the scores.

For fixed scores on the same evaluation data, lowering the threshold flags at least as many cases. It can catch additional actual cancellations and add false alarms. Recall cannot decrease when there are actual positives; precision may decrease, but is not guaranteed to do so. Raising the threshold flags fewer cases and may miss more cancellations. Which threshold is useful depends on the business goal and cost of errors.

Worked example: three customers have scores 0.8, 0.4, 0.2 and actual outcomes cancel, cancel, stay. At threshold 0.5, only the first is flagged: TP=1, FP=0, FN=1, precision=100%, recall=50%. At threshold 0.3, the first two are flagged: TP=2, FP=0, FN=0, precision=100%, recall=100%. Lowering the threshold improves recall here without lowering precision; results depend on the added cases.

Choose thresholds using validation data and the intended error tradeoff. Keep the test set independent for final evaluation. A 0.5 threshold is an option, not a universal optimum.

## Your task — compare two thresholds

These six records are validation examples. Positive means cancellation during the target month.

| Customer | Cancellation score | Actual outcome |
|---|---:|---|
| A | 0.90 | Cancels |
| B | 0.80 | Stays |
| C | 0.60 | Cancels |
| D | 0.40 | Cancels |
| E | 0.30 | Stays |
| F | 0.10 | Stays |

Predict cancellation when score >= threshold, including equality.

1. At threshold 0.5, list the flagged customers and give TP, FP, FN, precision, and recall.
2. Repeat at threshold 0.3.
3. If the priority is catching every cancellation in these examples and extra false alarms are acceptable, which threshold would you choose? Explain the tradeoff. This tiny example does not establish performance on future data.

Show your fractions and round percentages to one decimal place where needed. No coding or AWS resources needed. Completion requires reviewed threshold application and metric calculations.
