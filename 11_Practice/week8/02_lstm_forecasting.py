"""
Exercise 2: Time-Series Forecasting with LSTM
Multi-step forecast: given the last LOOKBACK values, predict the next HORIZON values.
Dataset: Daily Minimum Temperatures (Melbourne), columns Date and Temp.
  kaggle datasets download -d paulbrabban/daily-minimum-temperatures-in-melbourne -p data --unzip
Usage: python 02_lstm_forecasting.py path/to/your.csv
"""
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from sklearn.preprocessing import MinMaxScaler

PATH = sys.argv[1] if len(sys.argv) > 1 else "data/daily-minimum-temperatures.csv"
LOOKBACK = 30    # days of history fed to the model
HORIZON = 7      # days to predict ahead


def windows(values, L, H):
    """Sliding windows. T0 is the index of each target's first step, used for chronological splits."""
    X, Y, T0 = [], [], []
    for i in range(len(values) - L - H + 1):
        X.append(values[i:i + L])
        Y.append(values[i + L:i + L + H])
        T0.append(i + L)
    return np.array(X)[..., None], np.array(Y), np.array(T0)


def metrics(actual, pred):
    err = pred - actual
    return np.abs(err).mean(), np.sqrt((err ** 2).mean())


if __name__ == "__main__":
    tf.keras.utils.set_random_seed(42)

    df = pd.read_csv(PATH, parse_dates=[0])
    df = df.sort_values(df.columns[0]).reset_index(drop=True)
    series = df.iloc[:, 1].astype(float)
    print("Rows:", len(series), " Date range:", df.iloc[0, 0].date(), "to", df.iloc[-1, 0].date())
    print("Missing values:", int(series.isna().sum()))
    series = series.interpolate().values          # fill any gaps in time order

    fig, ax = plt.subplots(figsize=(12, 3.5))
    ax.plot(df.iloc[:, 0], series, lw=0.8)
    ax.set_title("Raw series"); ax.set_ylabel("Temp")
    plt.tight_layout(); plt.savefig("02_raw_series.png", dpi=120); plt.close()

    # Chronological split: 70% train, 15% val, 15% test. Never shuffle time series across the split.
    n = len(series)
    tr_end, va_end = int(0.70 * n), int(0.85 * n)

    # Scale using training data only.
    scaler = MinMaxScaler().fit(series[:tr_end, None])
    scaled = scaler.transform(series[:, None]).ravel()

    X, Y, T0 = windows(scaled, LOOKBACK, HORIZON)
    # A window belongs to a split if its entire target falls inside that split's period.
    train = T0 + HORIZON <= tr_end
    val = (T0 >= tr_end) & (T0 + HORIZON <= va_end)
    test = T0 >= va_end
    print(f"Windows: train={train.sum()}  val={val.sum()}  test={test.sum()}")

    inv = lambda a: scaler.inverse_transform(a.reshape(-1, 1)).reshape(a.shape)
    Y_te_real = inv(Y[test])

    # Baseline: persistence (tomorrow = today). Hard to beat on smooth series; always report it.
    naive_pred = np.repeat(inv(X[test][:, -1, 0])[:, None], HORIZON, axis=1)
    print("\nNaive persistence baseline (MAE, RMSE) by horizon:")
    for h in range(HORIZON):
        mae, rmse = metrics(Y_te_real[:, h], naive_pred[:, h])
        print(f"  day {h + 1}: MAE={mae:.3f}  RMSE={rmse:.3f}")

    model = keras.Sequential([
        keras.Input(shape=(LOOKBACK, 1)),
        keras.layers.LSTM(64),
        keras.layers.Dropout(0.2),
        keras.layers.Dense(HORIZON),
    ])
    model.compile(optimizer=keras.optimizers.Adam(1e-3), loss="mse", metrics=["mae"])
    early = keras.callbacks.EarlyStopping(monitor="val_loss", patience=10, restore_best_weights=True)
    hist = model.fit(X[train], Y[train], validation_data=(X[val], Y[val]),
                     epochs=100, batch_size=32, callbacks=[early], verbose=2)

    lstm_pred = inv(model.predict(X[test], verbose=0))
    print("\nLSTM (MAE, RMSE) by horizon:")
    for h in range(HORIZON):
        mae, rmse = metrics(Y_te_real[:, h], lstm_pred[:, h])
        print(f"  day {h + 1}: MAE={mae:.3f}  RMSE={rmse:.3f}")
    mae_all, rmse_all = metrics(Y_te_real, lstm_pred)
    mae_n, rmse_n = metrics(Y_te_real, naive_pred)
    print(f"\nOverall  LSTM: MAE={mae_all:.3f} RMSE={rmse_all:.3f}   "
          f"Naive: MAE={mae_n:.3f} RMSE={rmse_n:.3f}")
    model.save("lstm_forecaster.keras")

    dates_te = df.iloc[T0[test] + LOOKBACK, 0].values
    fig, ax = plt.subplots(2, 1, figsize=(12, 7))
    ax[0].plot(dates_te, Y_te_real[:, 0], label="actual (day +1)", lw=1)
    ax[0].plot(dates_te, lstm_pred[:, 0], label="LSTM (day +1)", lw=1)
    ax[0].plot(dates_te, naive_pred[:, 0], label="naive (day +1)", lw=1, alpha=0.6)
    ax[0].set_title("Test period, one-day-ahead forecast"); ax[0].legend()
    ax[1].plot(hist.history["loss"], label="train"); ax[1].plot(hist.history["val_loss"], label="val")
    ax[1].set_title("MSE loss (scaled)"); ax[1].set_xlabel("Epoch"); ax[1].legend()
    plt.tight_layout(); plt.savefig("02_forecast_results.png", dpi=120); plt.close()
    print("Saved 02_forecast_results.png and lstm_forecaster.keras")
