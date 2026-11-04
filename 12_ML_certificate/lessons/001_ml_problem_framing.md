# Assignment 001 — Frame an ML problem

Module: 00. Suggested time: 10–15 minutes. Status: First submission reviewed; correction pending.

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

Awaiting correction submission. Assignment remains incomplete until reviewed.
