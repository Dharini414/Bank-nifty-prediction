import yfinance as yf
import pandas as pd
import os
from datetime import datetime
import time

FILE_NAME = "banknifty_data.csv"
LOG_FILE = "log.txt"


def write_log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")


def fetch_data():
    start_time = time.time()

    write_log("=" * 60)
    write_log("Script Started")

    rows_added = 0

    # =========================
    # EXISTING FILE CASE
    # =========================
    if os.path.exists(FILE_NAME):
        old_data = pd.read_csv(FILE_NAME)
        old_data['Date'] = pd.to_datetime(old_data['Date'])

        last_date = old_data['Date'].max()
        start_date = last_date + pd.Timedelta(days=1)

        write_log(f"Fetching from {start_date.date()}")

        today = pd.Timestamp.today().normalize()
        if start_date > today:
            write_log("No new data to fetch (already up-to-date)")
            write_log("Status: SUCCESS")
            return 0

        data = yf.download(
            "^NSEBANK",
            start=start_date,
            interval="1d",
            progress=False,
            threads=False
        )

    # =========================
    # FIRST RUN CASE
    # =========================
    else:
        write_log("First time full download")

        data = yf.download(
            "^NSEBANK",
            start="2014-01-01",
            interval="1d",
            progress=False,
            threads=False
        )

    # =========================
    # NO DATA CASE
    # =========================
    if data.empty or data.isna().all().all():
        write_log("No valid new data (Market closed or no update)")
        write_log("Status: SUCCESS")
        return 0

    # =========================
    # CLEAN DATA
    # =========================
    data.reset_index(inplace=True)
    data = data.iloc[:, :6]
    data.columns = ['Date', 'Close', 'High', 'Low', 'Open', 'Volume']

    rows_added = len(data)

    # =========================
    # SAVE DATA
    # =========================
    if os.path.exists(FILE_NAME):
        combined = pd.concat([old_data, data])
        combined.drop_duplicates(subset=['Date'], inplace=True)
        combined.sort_values(by='Date', inplace=True)
        combined.to_csv(FILE_NAME, index=False)

        write_log(f"CSV updated | Rows added: {rows_added}")

    else:
        data.to_csv(FILE_NAME, index=False)
        write_log(f"New CSV created | Rows added: {rows_added}")

    # =========================
    # FINAL LOG
    # =========================
    execution_time = round(time.time() - start_time, 2)

    write_log(f"Execution Time: {execution_time} sec")
    write_log("Status: SUCCESS")

    return rows_added   # ✅ CRITICAL FOR PIPELINE


if __name__ == "__main__":
    try:
        rows = fetch_data()
        write_log(f"Final Rows Added: {rows}")
    except Exception as e:
        write_log("Status: FAILED")
        write_log(f"Error: {str(e)}")