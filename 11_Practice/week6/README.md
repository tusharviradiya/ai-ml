# Week 6: ANN for Classification, Regression, and Regularization

## Setup
```bash
pip install numpy pandas matplotlib scikit-learn tensorflow kaggle
kaggle competitions download -c titanic -p data && unzip data/titanic.zip -d data
kaggle competitions download -c house-prices-advanced-regression-techniques -p data
unzip data/house-prices-advanced-regression-techniques.zip -d data
mv data/house-prices-advanced-regression-techniques/train.csv data/house_train.csv
```
(Kaggle requires an API token and accepting the competition rules once in the browser.)

## Files
| File | Purpose |
|---|---|
| `titanic_prep.py` | Shared preprocessing: feature engineering, imputation, encoding, scaling. Fit on train only. |
| `01_ann_classification.py` | EDA, then a classification ANN on Titanic. Reports accuracy, F1, ROC-AUC, confusion matrix. |
| `02_ann_regression.py` | EDA, then a regression ANN on house prices. Reports MAE, RMSE, R², RMSLE, with a mean baseline. |
| `03_regularization_experiment.py` | Dropout, BatchNorm, and Early Stopping applied one at a time and combined, 3 seeds each. |

## Design decisions
- **Stratified splits** (classification) keep the survival rate the same across train, validation, and test.
- **Preprocessing is fit on the training split only**, so validation and test rows never influence imputation medians, scaling statistics, or category levels.
- **Log target for regression.** SalePrice is right-skewed. Training on `log1p` makes the loss less dominated by a few expensive houses, and RMSLE is the Kaggle metric.
- **Test set is touched once** at the end of each script.
- **Regularization experiment varies one thing at a time** (plus one combined run), with a fixed learning rate and architecture, so each effect is attributable.

## Metrics: when to use which
- Accuracy can mislead on imbalanced data. Check F1 and ROC-AUC too.
- For regression, MAE is in dollars and easy to interpret. RMSE penalizes large errors more. R² shows how much variance the model explains. RMSLE treats percentage errors evenly across cheap and expensive houses.

## Results and what helped
Fill in after running. Use `03_summary.csv` for the regularization table.

### Classification (Titanic)
- Test accuracy / F1 / ROC-AUC:
- Early-stopping epoch and whether restored weights helped:

### Regression (House prices)
- Test MAE / RMSE / R² / RMSLE, compared with the mean baseline:
- Did the log target help? (Optional: rerun with raw SalePrice and compare.)

### Regularization
- Which technique most reduced the validation-train gap:
- Which improved test AUC, and by how much relative to seed variance:
- Did BatchNorm and Dropout help together, or did they interfere?
- Was early stopping the biggest win? Compare the baseline's final epoch with the early-stopped run's best epoch.
- Caveat: the Titanic test set is about 180 rows, so differences under about 0.02 in accuracy are within noise.
