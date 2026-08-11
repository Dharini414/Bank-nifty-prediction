import pandas as pd
import os
from datetime import datetime
import time

RAW_FILE = "banknifty_data.csv"
FEATURE_FILE = "features.csv"
LOG_FILE = "features_log.txt"


def write_log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")


def add_indicators(df):
    df = df.copy()

    # =========================
    # MOVING AVERAGES
    # =========================
    df['SMA_50'] = df['Close'].rolling(50).mean()
    df['SMA_100'] = df['Close'].rolling(100).mean()

    df['EMA_12'] = df['Close'].ewm(span=12, adjust=False).mean()
    df['EMA_26'] = df['Close'].ewm(span=26, adjust=False).mean()

    # =========================
    # RSI
    # =========================
    delta = df['Close'].diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = -delta.clip(upper=0).rolling(14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))

    # =========================
    # MACD
    # =========================
    df['MACD'] = df['EMA_12'] - df['EMA_26']
    df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()
    df['MACD_Hist'] = df['MACD'] - df['Signal_Line']

    # =========================
    # BOLLINGER BANDS
    # =========================
    sma_20 = df['Close'].rolling(20).mean()
    std_20 = df['Close'].rolling(20).std()

    df['BB_Upper'] = sma_20 + (2 * std_20)
    df['BB_Lower'] = sma_20 - (2 * std_20)

    # =========================
    # MOMENTUM
    # =========================
    df['Momentum'] = df['Close'] - df['Close'].shift(10)

    # =========================
    # RETURNS (FIXED)
    # =========================
    df['Return_1D'] = df['Close'].pct_change(fill_method=None)
    df['Return_5D'] = df['Close'].pct_change(5, fill_method=None)
    df['Return_10D'] = df['Close'].pct_change(10, fill_method=None)

    # =========================
    # VOLATILITY
    # =========================
    df['Volatility_10'] = df['Return_1D'].rolling(10).std()
    df['Volatility_20'] = df['Return_1D'].rolling(20).std()

    # =========================
    # TREND FEATURES
    # =========================
    df['Price_vs_SMA50'] = df['Close'] / df['SMA_50']
    df['Price_vs_SMA100'] = df['Close'] / df['SMA_100']

    # =========================
    # TARGET (FIXED)
    # =========================
    
    return df


def compute_features():
    start_time = time.time()
    rows_added = 0

    write_log("="*60)
    write_log("Feature Script Started")

    if not os.path.exists(RAW_FILE):
        write_log("Raw CSV not found")
        write_log("Status: FAILED")
        return 0

    raw = pd.read_csv(RAW_FILE)
    raw['Date'] = pd.to_datetime(raw['Date'])
    raw = raw.sort_values(by='Date')

    # =========================
    # FIRST RUN
    # =========================
    if not os.path.exists(FEATURE_FILE):
        write_log("First run: computing full dataset")

        features = add_indicators(raw)
        features = features.dropna()   # ✅ FIXED
        features = features.reset_index(drop=True)

        features.to_csv(FEATURE_FILE, index=False)

        rows_added = len(features)
        write_log(f"Features CSV created | Rows: {rows_added}")

    else:
        features_old = pd.read_csv(FEATURE_FILE)
        features_old['Date'] = pd.to_datetime(features_old['Date'])

        last_feature_date = features_old['Date'].max()

        new_rows = raw[raw['Date'] > last_feature_date]

        if new_rows.empty:
            write_log("No new rows to process")
            write_log("Status: SUCCESS")
            return 0

        write_log(f"New rows detected: {len(new_rows)}")

        # =========================
        # FIX: use RAW data only
        # =========================
        tail_old = raw[raw['Date'] <= last_feature_date].tail(120)

        combined = pd.concat([tail_old, new_rows])
        combined = combined.drop_duplicates(subset=['Date'])
        combined = combined.sort_values(by='Date').reset_index(drop=True)

        updated = add_indicators(combined)
        updated = updated.dropna()   # ✅ FIXED

        updated_new = updated[updated['Date'] > last_feature_date]

        rows_added = len(updated_new)

        final = pd.concat([features_old, updated_new])
        final = final.drop_duplicates(subset=['Date'])
        final = final.sort_values(by='Date').reset_index(drop=True)

        final.to_csv(FEATURE_FILE, index=False)

        write_log(f"Appended rows: {rows_added}")

    execution_time = round(time.time() - start_time, 2)
    write_log(f"Execution Time: {execution_time} sec")
    write_log("Status: SUCCESS")

    return rows_added


if __name__ == "__main__":
    try:
        rows = compute_features()
        write_log(f"Final Rows Added: {rows}")
    except Exception as e:
        write_log("Status: FAILED")
        write_log(f"Error: {str(e)}")