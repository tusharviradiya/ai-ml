# Assignment 002 — Training, validation, and test data

Module: 00. Suggested time: 15–20 minutes. Status: Complete after guided corrections; retention and precise terminology require later recall. Historical tasks below are preserved.

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

## Submission 1 — original wording (5 November 2026)

> 1. 150 images.
> 2. which have batter percentage on validation test, i will choose that candidate model
> 3. because this repeatedly change model based on resultes is take much time and cost also thats why ig.

## Review 1

- Answer 1 is incomplete: 150 is correct for each of validation and test, but training needs 700. Calculation: 1,000 × 70/100 = 700; 1,000 × 15/100 = 150 for each remaining group.
- Answer 2 correctly uses validation performance for candidate selection. Call this the validation set to distinguish it from the separate test set. "Better" depends on the metric selected for the task; not every metric is a percentage or improved by increasing it.
- Answer 3 identifies a possible resource cost, but misses the main statistical reason. Final evaluation uses the test set. Repeated changes guided by its results adapt development to that particular set, so its score becomes an optimistic basis for judging new data. The test set loses its role as an independent final check even if no test records are directly used to fit model parameters.
- Analogy: repeatedly checking the same final exam and changing preparation to improve that score does not demonstrate equally good performance on a fresh exam. Use validation for development choices and preserve test data for final evaluation.

## Current task — targeted correction

For 2,000 independent images and the same 70/15/15 split:

1. Give all three counts: training, validation, and test.
2. A developer checks test results after every model change and keeps whichever version scores best on that test set. Why might its reported test score be misleading? Which set should guide these development choices?

Reply with answers 1–2. Assignment remains active; completed assignment count remains 1 overall.

## Submission 2 — original wording (5 November 2026)

> 1. 1400 / 300 / 300
> 2. test score is not god for good choices, we need to check validation score.

## Review 2

- All split counts are correct in the requested order: 1,400 training, 300 validation, 300 test.
- Correctly selects validation results for development choices. The explanation of why repeated test-based selection is misleading is still missing.
- Clarification: a test score is useful for final evaluation when the test data has been kept independent. Repeated test-based selection can exploit quirks of that particular sample; a higher score may not carry over to fresh examples. This is often called overfitting to the test set, even when test records never directly enter model fitting.
- Worked example: a developer tries many settings and keeps only those that raise accuracy on the same 300 test images. Eventually the score reaches 98%. Because those test results guided the changes, 98% may overestimate accuracy on new images. Use validation for those choices and a separate untouched test set for the final check.

## Current task — one explanation

A developer makes 20 model changes based on the same test set and finally obtains 98% accuracy. Why might accuracy on brand-new images be lower? Explain in your own words in one or two sentences. No need to repeat the split counts.

Assignment remains active pending this explanation; overall completed count remains 1.

## Submission 3 — original wording (5 November 2026)

> if we overtrain our model based on our limited dataset, so thsi will overperforme on new image, this called overfitting, and this is problem for us because we loose our 98% accurance drastically on next new image prediction.

## Review 3 and completion

- Identifies overfitting and recognizes that the reported 98% may not carry over to new images. This supports introductory understanding when combined with the correct split counts and validation selection in earlier answers.
- Wording correction: a model may perform worse on new images, not better. A drop is possible, but neither its size nor a drastic drop is established by the scenario. Accuracy measures performance over a collection of examples; one image prediction is simply correct or incorrect.
- Mechanism clarification: here the problem is repeated model selection using test results. It can compromise test independence even without training for more iterations or directly fitting on test records. Overtraining can cause some forms of overfitting, but is not required for test-based selection bias.
- Mark Assignment 002 complete after guided corrections; revisit this mechanism in later recall. Next: Assignment 003, recognizing overfitting and underfitting from training/validation results.
