# Assignment 002 — Training, validation, and test data

Module: 00. Suggested time: 15–20 minutes. Status: Assigned; awaiting first submission.

## Lesson

A model needs evaluation on examples it did not learn from. Otherwise, remembering training examples can look like the ability to handle new examples.

Separate data into three groups:

| Group | Purpose | Exam analogy |
|---|---|---|
| Training | Fit the model: learn its parameters from examples | Study worked examples |
| Validation | Compare candidate models/settings and choose between them | Use practice exams to guide preparation |
| Test | Assess the chosen model after development decisions are finished | Take a final exam whose answers were not used for preparation |

Validation and test labels are used to calculate evaluation metrics. They are not used to fit model parameters in this introductory workflow. Validation results influence model choice; test results should not repeatedly guide changes. Repeatedly adapting to the test set makes it part of development and weakens its independence.

Example: with 1,000 independent labeled examples, a possible split is 700 training, 150 validation, and 150 test. This 70/15/15 ratio is illustrative, not mandatory. Train candidate models on the 700 examples, compare them using the 150 validation examples, then evaluate the chosen model on the 150 test examples.

Split strategy matters: future-prediction problems often need chronological evaluation; related records may need to stay in the same group. A random split is not automatically valid. Learn preprocessing statistics from training data only, then apply the same transformation to validation and test data. These topics will receive later practical treatment.

## Your task — one scenario

You have 1,000 independent labeled product images for a classification task. For this exercise, use a 70/15/15 split. No duplicate or related images cross the groups.

1. How many images go into training, validation, and test?
2. You train two candidate models. Which group do you use to choose between them?
3. After choosing, which group gives the final evaluation? Why should you avoid repeatedly changing the model based on this group's results?

Reply with answers 1–3. No coding or AWS resources are needed.

## Review criteria

Correct counts; training distinguished from model selection and final evaluation; explanation that repeatedly using test results to guide changes compromises an independent assessment. No completion until reviewed.
