from flask import Flask, jsonify
import pandas as pd
import numpy as np
import joblib

app = Flask(__name__)

MODEL_FILE = "xgb_model.pkl"
DATA_FILE = "features.csv"

model = joblib.load(MODEL_FILE)

FEATURES = [
    'Return_1D',
    'Return_1D_lag1',
    'Momentum',
    'Momentum_lag1',
    'RSI',
    'MACD',
    'MACD_Hist',
    'rolling_return_5',
    'Price_vs_SMA50'
]


def load_data():

    df = pd.read_csv(DATA_FILE, parse_dates=["Date"])

    df = df.sort_values("Date").reset_index(drop=True)

    # Missing engineered features

    df["RSI_lag1"] = df["RSI"].shift(1)
    df["MACD_lag1"] = df["MACD"].shift(1)
    df["Momentum_lag1"] = df["Momentum"].shift(1)
    df["Return_1D_lag1"] = df["Return_1D"].shift(1)

    df["trend_5"] = df["Close"].shift(1).rolling(5).mean()
    df["trend_10"] = df["Close"].shift(1).rolling(10).mean()

    df["rolling_std_5"] = df["Close"].shift(1).rolling(5).std()
    df["rolling_return_5"] = (
        df["Return_1D"]
        .shift(1)
        .rolling(5)
        .sum()
    )

    df = df.replace([np.inf, -np.inf], np.nan)

    df = df.dropna().reset_index(drop=True)

    return df


@app.route("/predict", methods=["GET"])
def predict():

    try:

        df = load_data()

        latest_row = df.iloc[-1]

        X = latest_row[FEATURES].values.reshape(1, -1)

        prediction = float(model.predict(X)[0])

        historical_predictions = model.predict(df[FEATURES])

        buy_threshold = np.quantile(
            historical_predictions,
            0.90
        )

        sell_threshold = np.quantile(
            historical_predictions,
            0.10
        )

        if prediction >= buy_threshold:
            signal = "BUY"

        elif prediction <= sell_threshold:
            signal = "SELL"

        else:
            signal = "HOLD"

        future_date = (
            latest_row["Date"]
            + pd.Timedelta(days=1)
        )

        return jsonify({

            "prediction_date":
                str(future_date.date()),

            "predicted_return":
                prediction,

            "signal":
                signal,

            "buy_threshold":
                float(buy_threshold),

            "sell_threshold":
                float(sell_threshold)

        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)