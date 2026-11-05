# Assignment 003 — Overfitting and underfitting

Module: 00. Suggested time: 15–20 minutes. Status: Assigned; awaiting first submission.

## Lesson

Generalization means performing well on new examples from the intended use case.

- Underfitting: the model has not learned enough useful structure. It performs poorly even on training data, often with poor validation performance too. A model that is too simple or insufficiently trained can underfit.
- Overfitting: the model fits training-specific details or noise that do not carry over well. High training performance with substantially lower validation performance is a warning sign.
- A promising fit: training and validation performance are both good and reasonably close. This does not by itself prove readiness or rule out leakage.

Worked example: a model scores 99% training accuracy and 68% validation accuracy. The 31 percentage-point gap suggests overfitting, assuming valid, comparable splits and a suitable metric. Possible responses include regularization (penalizing excessive complexity), a simpler model, more representative training examples, or early stopping (stop when validation performance stops improving). Select changes using validation data, not test results.

Underfitting may call for better features, a more expressive model, or more training if learning is still improving. These choices depend on the cause; more training is not a universal solution.

Accuracy is the fraction of correct predictions across examples. It is useful in this simplified exercise; later lessons cover situations where accuracy is misleading, such as imbalanced classes.

## Your task — compare three models

All models predict the same balanced classification task. Assume representative, independent splits with no leakage and that 95% accuracy is useful for this exercise.

| Model | Training accuracy | Validation accuracy |
|---|---:|---:|
| A | 99% | 70% |
| B | 60% | 59% |
| C | 96% | 95% |

1. Which model shows signs of overfitting? Explain using both scores.
2. Which model shows signs of underfitting? Explain using both scores.
3. Which model would you choose for final testing, and why?

Reply with answers 1–3. No coding or AWS resources needed. Completion requires review; these patterns are diagnostic clues rather than proof of a single cause.

## Clarification before submission (5 November 2026)

Learner question, original wording:

> before give answer of my assignment 3,
> can you tell me that,
> 1. if my training accurancy is 35% and valication accurancy is 30% so this is good? or this is underfeeting problem?

Explanation: close scores alone do not establish a good model. Check both their absolute usefulness against an appropriate baseline and their gap. If 35% training and 30% validation are both poor for the task, this pattern suggests underfitting or another learning/data issue, rather than a successful fit. The gap is 5 percentage points, but both scores can still be inadequate.

Context matters: on a balanced two-class task, a constant majority-class prediction achieves 50%, so these scores are worse than that simple baseline and merit checking features, labels, implementation, model capacity, and training. On a balanced 10-class task, uniform guessing averages 10%, so 30% validation beats that baseline but may still be insufficient for the intended use. These two scores alone cannot prove underfitting or identify its cause.

Working rule: good and close is promising; poor and close suggests underfitting/learning problems; high training and much lower validation suggests overfitting. Interpret these as diagnostic clues within the task context. Assignment 003 remains awaiting its original submission; no extra task or completion recorded.
