# Assignment 001 — Frame an ML problem

Module: 00. Suggested time: 10–15 minutes. Status: Complete after guided corrections; later recall scheduled through subsequent lessons. Historical tasks and reviews below are preserved.

5 November 2026 planning note: lesson progression is on hold at the learner's request while the Skill Builder Premium plan is reviewed. The original submission and correction task below remain preserved; no completion has been recorded.

Subsequent update: learner agreed to begin after the November plan was set. Learning has resumed; the correction exercise below is active and awaiting submission.

No coding, AWS account, or external reading is needed. Reply in chat; the tutor will save your submission and review here.

## Lesson

An ML project begins by stating what to predict, when to predict it, and what information exists at that time.

- **Features:** inputs available when making a prediction.
- **Label/target:** the outcome the model learns to predict from historical examples in supervised learning.
- **Classification:** predicts a category; binary classification has two possible categories.
- **Regression:** predicts a numeric quantity such as a price.
- **Training:** learns model parameters from historical examples.
- **Inference:** uses a trained model to make a prediction on an input.
- **Data leakage:** uses information during development or evaluation that would not legitimately be available for the intended prediction. This can make evaluation misleadingly good.

### Worked example

Suppose we predict a home's sale price before it sells.

- Features: floor area, number of bedrooms, and location known at prediction time.
- Label: actual sale price from completed historical sales.
- Problem type: regression, because price is a numeric quantity.
- Training: learning relationships from historical homes and their sale prices.
- Inference: estimating the sale price of a new home.
- Leakage example: using the final sale receipt amount as an input to predict that same sale price.

Historical outcome labels are necessary for supervised training. The leakage problem is exposing unavailable future information through inputs or the development/evaluation process, rather than using labels to learn.

## Your task — subscription cancellation

On **1 November**, a subscription company predicts whether each currently subscribed customer will cancel **during November**.

Candidate data fields:

| Field | Availability |
|---|---|
| Number of logins during October | Known on 1 November |
| Subscription plan on 1 November | Known at prediction time |
| Support tickets opened during October | Known on 1 November |
| Actual cancellation date during November, if any | Known only later |

Answer these five questions in your own words:

1. Is this classification or regression? Why?
2. What exactly is the label for each customer?
3. Which three fields would you use as features, and why are they valid at prediction time?
4. Why would using the actual November cancellation date as an input be leakage?
5. Describe training and inference for this company in one sentence each.

Reply using numbers 1–5. If unsure, explain your thinking rather than guessing silently.

## Review criteria

The learner must distinguish a category from a numeric outcome, define the cancellation window, choose inputs available at the prediction time, explain future-information leakage, and distinguish learning from applying a model. No numeric score is assigned before reviewing the submission.

## Learner submission

### Submission 1 — original wording

> 1. classification
> 2. yes and no
> 3. current subscription plan, number of october support ticketes, actual noverber cancellation date
> 4. subscripion is wary date based on subscrioption so we don't take it.
> 5. don't know.

## Tutor review

### Review 1

1. Correct problem type. It is binary classification because the outcome has two categories.
2. Correct categories. Define them precisely: yes = cancels during November; no = does not cancel during November.
3. Partially correct. The valid inputs are October logins, the current plan, and October support tickets. The November cancellation date is not yet known on 1 November.
4. Needs correction. The issue is future-information availability, not the fact that the field is a date. A date known before prediction can be a valid input. The actual November cancellation date reveals the future outcome being predicted.
5. Not yet understood. Training learns from historical inputs and known outcomes. Inference applies the trained model to inputs whose outcome is not yet known.

### Reinforcement: learning versus predicting

Imagine that historical records show September activity and whether each customer canceled during October. On 1 November, both are known, so they can be used for training. The model learns relationships from many such examples; these relationships are not guarantees for every customer.

On 1 November, give the trained model October activity and the current plan to predict November cancellation. That is inference. November's outcome is still unknown.

Known historical outcomes are used as training labels, not smuggled into the inputs for a prediction made before those outcomes occurred.

### Current task — three-part correction

Reply in your own words:

1. List the three valid features for the original November prediction. Explain why the actual November cancellation date is excluded.
2. A model learns from September activity and known October cancellation outcomes. Is this training or inference? Why?
3. On 1 November, that trained model uses October activity to predict November cancellation. Is this training or inference? State the two possible label values and the month they refer to.

### Submission 2 — original wording (5 November 2026)

> 1. october support tickets.
> 2. training 
> 3. now as of now we are making prediction then its inference.

### Review 2

- October support tickets are a valid feature, but the answer omits October logins and the current subscription plan. All three are available on 1 November. The requested exclusion explanation is still missing.
- Correctly identified training. The reason is that the model is learning patterns from historical examples with known outcomes; this reason still needs independent confirmation.
- Correctly identified inference and explained that the model is making a prediction. The two requested outcomes and their November time window were omitted.
- Progress: training/inference identification has improved. Feature availability and leakage still need a focused application check; no completion recorded.

### Reinforcement and next check

Several fields can be valid inputs together. October logins, the current plan, and October support tickets are all known on 1 November. The actual November cancellation date is future information: using it as an input would reveal the outcome. The labels are cancels during November / does not cancel during November.

Transfer example: on 1 December, predict whether a current subscriber will cancel during December. Candidate inputs are November logins, the current plan, November support tickets, and the actual December cancellation date.

Reply with all valid inputs and explain why the remaining field is excluded. Then state the two possible December outcomes. Assignment 001 remains active pending this check; training reasoning can be checked in later recall.

### Additional explanation requested — data leakage (5 November 2026)

Learner request:

> before moving on practice task,
> can you more explain me about data leakage?

The transfer exercise remains pending while this concept is explained. No new assignment or mastery credit is added.

Data leakage happens when information that should be unavailable for the intended prediction or independent evaluation influences the model. It can make evaluation look better than performance on genuinely new cases.

Analogy: seeing an answer key before a practice exam can improve the practice score without improving the ability to answer new questions. Leakage can happen accidentally through data preparation.

For a prediction made on 1 November:

| Field | Use as input? | Reason |
|---|---|---|
| October logins | Yes | Already recorded at prediction time |
| Plan as it stood on 1 November | Yes | Known at prediction time |
| October support tickets | Yes | Already recorded at prediction time |
| Actual November cancellation date | No | Reveals an outcome that occurs after prediction time |
| November cancellation refund | No | A consequence of the future cancellation; can indirectly reveal the outcome |

In a completed historical dataset, November's outcome may now be known. Still reconstruct each example using only information available at its original prediction time. Keep the later outcome as the supervised learning label, not as an input.

Labels during training are expected: October inputs -> model prediction -> compare with known November outcome -> adjust model. Feeding the actual November cancellation date into those inputs gives away the answer.

Dates are not automatically leakage. A customer's signup date known on 1 November can be valid. The issue is when the information became available and what it reveals.

Leakage can also affect evaluation: if identical records appear in both training and test sets, a model can appear to generalize while recognizing examples it has already seen. Fitting preprocessing, such as missing-value averages, on the whole dataset before splitting also allows held-out information to influence training. Fit learned preprocessing on training data and apply it unchanged to held-out data. Detailed splitting practice will follow later.

Working checks: Could this value really be known when the prediction is made? Was it created as a consequence of the outcome? Has held-out evaluation data influenced model fitting, preprocessing, or model selection? These checks help identify leakage; they do not establish mastery until the learner applies them.

### Submission 3 — original wording (5 November 2026)

> subscriber will cancle during december : 
> we train model based on november logins, their current plan, november support tickets, and as we exclude actual december cancellation dates because we don't have that info at 1st december.

### Review 3

- Correctly selected all three available inputs and explained that actual December cancellation dates are unavailable on 1 December. Prediction-time feature availability and future-outcome leakage are demonstrated in this transfer example; retain for later recall.
- The phrase "we train model" needs clarification: using these inputs on 1 December to predict December cancellation with an already trained model is inference. For supervised training on this same target, the November inputs need known December outcomes, which are not available yet. Earlier completed periods can supply historical training pairs.
- The learner named cancellation during December but did not explicitly state both outcomes. These are cancels during December / does not cancel during December.
- Assignment remains active for a short training/inference application check; no need to repeat the passed feature-selection exercise.

### Current task — training/inference application

Worked distinction: learn from September activity and known October cancellation outcomes = training. Apply that trained model to November activity on 1 December to predict December cancellation = inference.

Check: a model learns from October activity and known November cancellation outcomes. Is this training or inference, and why? Reply in one sentence. Label-window and classification reasoning can be revisited in later recall.

### Submission 4 — original wording (5 November 2026)

> its training because we have all required data.

### Review 4 and completion

- Correctly identifies training in the historical learning scenario. "All required data" includes both historical inputs and known outcome labels; the defining action is learning from those examples. Merely having data does not by itself make an operation training.
- Together with earlier submissions, this establishes sufficient introductory understanding to advance: classification/categories identified, available features selected, future-outcome leakage explained, and training/inference recognized after guidance.
- Assignment 001 marked complete after guided corrections, not as evidence of independent mastery of every concept. Later recall will check classification reasoning, labels with an explicit time window, and the learning-versus-predicting distinction.
- Next assignment: 002 — Training, validation, and test data. Module 00 remains in progress.
