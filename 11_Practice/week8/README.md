# Week 8: RNNs, LSTMs, and GRUs

## Setup
```bash
pip install tensorflow pandas scikit-learn matplotlib kaggle numpy
```
Exercises 1 and 3 need no downloads. Exercise 3 downloads IMDB through Keras on first run.

For exercise 2, download a daily time series. The default is the Melbourne minimum temperatures dataset:
```bash
kaggle datasets download -d paulbrabban/daily-minimum-temperatures-in-melbourne -p data --unzip
```
Check the CSV's column names. The script expects the date in column 1 and the value in column 2.
Pass any other daily CSV with `python 02_lstm_forecasting.py path/to/file.csv`.

Exercise 3 benefits from a GPU. The CPU run takes a few minutes per model.

## Files
| File | Purpose |
|---|---|
| `01_rnn_fundamentals.py` | SimpleRNN vs LSTM on a long-memory task, across sequence lengths |
| `02_lstm_forecasting.py` | Multi-step LSTM forecast, compared with a persistence baseline |
| `03_text_sentiment_lstm_gru.py` | LSTM vs GRU sentiment classifier on IMDB, 3 seeds each |

## Design decisions
- **Exercise 1 isolates memory.** The label depends only on step 0, so any accuracy loss as T grows
  is a memory failure, not a modeling failure. Chance is 0.5.
- **Chronological splitting in exercise 2.** Random splits leak future information into training.
  Scaling uses training data only. Windows are assigned to a split only if their whole target falls
  inside it. Shuffling training windows is fine because they only ever see training-period targets.
- **Always compare to a baseline.** Persistence (repeat the last value) is hard to beat on smooth
  series. An LSTM that does not beat it has not learned anything useful.
- **Same architecture for LSTM and GRU in exercise 3.** The only difference is the recurrent cell,
  so differences come from the cell. Padding is masked so the RNN skips padding tokens.

## Results
Fill in after running.

### Exercise 1: RNN limitations
- Test accuracy by sequence length, SimpleRNN vs LSTM:
- At what length does SimpleRNN drop to chance? Does the LSTM hold up longer?
- Why: the gradient through T steps of repeated multiplication either vanishes or explodes. The LSTM's
  additive cell state gives gradients a more direct path back. Discuss what you observed in your own words.

### Exercise 2: LSTM forecasting
- MAE and RMSE by horizon, LSTM vs naive:
- Does the LSTM beat persistence at day +1? At day +7?
- Look at `02_forecast_results.png`. Where does the forecast lag the actual series, for example at sudden changes?
- Did early stopping trigger? At what epoch?

### Exercise 3: LSTM vs GRU
- Mean test accuracy, parameter counts, and sec/epoch from `03_all_runs.csv`:
- Is the difference larger than the seed standard deviation?
- GRU has fewer parameters (three gates, not four). Did that show up in training time or accuracy?
- Why might sentiment be easy for both? Consider what a bag of words already captures.
