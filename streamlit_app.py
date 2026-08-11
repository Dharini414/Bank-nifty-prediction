import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="BankNifty Signal Dashboard",
    layout="wide"
)

st.title("📈 BankNifty Prediction Dashboard")

# ---------------------------------
# Load data
# ---------------------------------

df = pd.read_csv(
    "features.csv",
    parse_dates=["Date"]
)

df = df.sort_values("Date")

# ---------------------------------
# Prediction Section
# ---------------------------------

if st.button("Predict Next Trading Day"):

    response = requests.get(
        "http://127.0.0.1:5000/predict"
    )

    if response.status_code == 200:

        result = response.json()

        st.subheader(
            f"Prediction For: {result['prediction_date']}"
        )

        st.metric(
            "Predicted Future Return",
            f"{result['predicted_return']:.6f}"
        )

        signal = result["signal"]

        if signal == "BUY":
            st.success("🟢 BUY SIGNAL")

        elif signal == "SELL":
            st.error("🔴 SELL SIGNAL")

        else:
            st.warning("🟡 HOLD SIGNAL")

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "BUY Threshold",
                f"{result['buy_threshold']:.6f}"
            )

        with col2:

            st.metric(
                "SELL Threshold",
                f"{result['sell_threshold']:.6f}"
            )

    else:

        st.error(
            response.json().get(
                "error",
                "Prediction failed"
            )
        )

# ---------------------------------
# Market Trend Chart
# ---------------------------------

st.subheader("Market Trend")

chart_df = df.tail(250)

fig, ax = plt.subplots(figsize=(12, 5))

ax.plot(
    chart_df["Date"],
    chart_df["Close"]
)

ax.set_title("BankNifty Close Price")
ax.set_xlabel("Date")
ax.set_ylabel("Close")

st.pyplot(fig)

# ---------------------------------
# Latest Data
# ---------------------------------

st.subheader("Latest Market Data")

st.dataframe(
    df.tail(20),
    use_container_width=True
)