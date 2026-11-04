# Assignment 001 — Frame an ML problem

Module: 00. Suggested time: 10–15 minutes. Status: Awaiting submission.

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

Awaiting submission.

## Tutor review

Not reviewed. Do not mark this assignment complete until answers and any necessary corrections have been reviewed.
