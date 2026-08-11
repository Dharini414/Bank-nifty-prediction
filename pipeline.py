import time
from datetime import datetime

from nifty_data_fetch import fetch_data
from features import compute_features   # make sure filename = features.py


LOG_FILE = "pipeline_log.txt"


def write_log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")


def run_pipeline():
    start_time = time.time()

    write_log("=" * 60)
    write_log("Pipeline Started")

    try:
        # =========================
        # STEP 1: FETCH DATA
        # =========================
        write_log("Running Data Fetch Script...")
        rows_added = fetch_data()

        write_log(f"Fetch Completed | Rows Added: {rows_added}")

        # =========================
        # STEP 2: CONDITIONAL FEATURES
        # =========================
        if rows_added == 0:
            write_log("No new data → Skipping feature engineering")
            write_log("Status: SUCCESS")
            return

        write_log("Running Feature Engineering Script...")
        feature_rows = compute_features()

        write_log(f"Features Updated | Rows Added: {feature_rows}")

        # =========================
        # FINAL LOG
        # =========================
        execution_time = round(time.time() - start_time, 2)

        write_log(f"Total Execution Time: {execution_time} sec")
        write_log("Status: SUCCESS")

    except Exception as e:
        write_log("Status: FAILED")
        write_log(f"Error: {str(e)}")


if __name__ == "__main__":
    run_pipeline()
    