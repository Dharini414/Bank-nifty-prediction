import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="BankNifty Signal Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CONFIGURATION
# =========================================================

API_URL = "https://bank-nifty-prediction.onrender.compredict"

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background-color: #f8fafc;
    }

    /* Main content */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    /* Header */
    .dashboard-header {
        background: white;
        padding: 25px 30px;
        border-radius: 16px;
        border: 1px solid #e2e8f0;
        margin-bottom: 25px;
    }

    .dashboard-title {
        font-size: 32px;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 5px;
    }

    .dashboard-subtitle {
        color: #64748b;
        font-size: 15px;
    }

    /* Section headers */
    .section-title {
        font-size: 21px;
        font-weight: 650;
        color: #0f172a;
        margin-top: 25px;
        margin-bottom: 12px;
    }

    /* Metric cards */
    [data-testid="stMetric"] {
        background-color: white;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 18px;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
    }

    [data-testid="stMetricLabel"] {
        color: #64748b;
    }

    [data-testid="stMetricValue"] {
        color: #0f172a;
        font-weight: 700;
    }

    /* Buttons */
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        border: none;
        padding: 12px 20px;
        font-weight: 600;
        font-size: 15px;
        background-color: #0f172a;
        color: white;
    }

    .stButton > button:hover {
        background-color: #1e293b;
        color: white;
    }

    /* Dataframe */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: white;
        border-right: 1px solid #e2e8f0;
    }

    /* Small status card */
    .status-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 18px;
        margin-top: 15px;
    }

    .status-label {
        color: #64748b;
        font-size: 13px;
    }

    .status-value {
        color: #0f172a;
        font-size: 16px;
        font-weight: 600;
        margin-top: 4px;
    }

</style>
""", unsafe_allow_html=True)

# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    df = pd.read_csv(
        "features.csv",
        parse_dates=["Date"]
    )

    df = df.sort_values("Date")
    df = df.reset_index(drop=True)

    return df


try:
    df = load_data()

except Exception as e:

    st.error(f"Unable to load market data: {e}")
    st.stop()


# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="dashboard-header">

    <div class="dashboard-title">
        📈 BankNifty Prediction Dashboard
    </div>

    <div class="dashboard-subtitle">
        Machine Learning powered market signal analysis
        using technical indicators and XGBoost.
    </div>

</div>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## ⚙️ Dashboard")

    st.markdown("---")

    st.markdown("### 📊 Data Information")

    latest_date = df["Date"].max()

    st.write(
        f"**Latest Data:**  "
        f"{latest_date.strftime('%d %b %Y')}"
    )

    st.write(
        f"**Total Records:**  "
        f"{len(df):,}"
    )

    st.markdown("---")

    st.markdown("### 🤖 Model")

    st.write("**Model:** XGBoost")

    st.write("**Prediction:** Next Trading Day")

    st.write("**Signals:** BUY / HOLD / SELL")

    st.markdown("---")

    st.caption(
        "⚠️ This dashboard is for educational "
        "and analytical purposes only."
    )


# =========================================================
# TOP MARKET STATISTICS
# =========================================================

latest_row = df.iloc[-1]

current_price = latest_row["Close"]

previous_price = (
    df.iloc[-2]["Close"]
    if len(df) > 1
    else current_price
)

daily_change = (
    (current_price - previous_price)
    / previous_price
) * 100


col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "BankNifty Close",
        f"{current_price:,.2f}",
        f"{daily_change:+.2f}%"
    )

with col2:

    st.metric(
        "RSI",
        f"{latest_row['RSI']:.2f}"
    )

with col3:

    st.metric(
        "Momentum",
        f"{latest_row['Momentum']:,.2f}"
    )

with col4:

    st.metric(
        "Price / SMA50",
        f"{latest_row['Price_vs_SMA50']:.3f}"
    )


# =========================================================
# PREDICTION SECTION
# =========================================================

st.markdown(
    '<div class="section-title">🤖 Next Trading Day Prediction</div>',
    unsafe_allow_html=True
)

prediction_col, info_col = st.columns([1.5, 1])

with prediction_col:

    if st.button(
        "🔮 Predict Next Trading Day",
        use_container_width=True
    ):

        with st.spinner("Connecting to prediction model..."):

            try:

                response = requests.get(
                    API_URL,
                    timeout=120
                )

                if response.status_code == 200:

                    result = response.json()

                    prediction_date = result[
                        "prediction_date"
                    ]

                    predicted_return = result[
                        "predicted_return"
                    ]

                    signal = result["signal"]

                    buy_threshold = result[
                        "buy_threshold"
                    ]

                    sell_threshold = result[
                        "sell_threshold"
                    ]

                    st.session_state["prediction"] = result

                else:

                    try:
                        error_message = response.json().get(
                            "error",
                            "Prediction failed"
                        )

                    except Exception:
                        error_message = (
                            "Prediction API returned an error."
                        )

                    st.error(error_message)

            except requests.exceptions.Timeout:

                st.error(
                    "Prediction API timed out. "
                    "The free Render service may be waking up."
                )

            except requests.exceptions.RequestException as e:

                st.error(
                    f"Could not connect to prediction API: {e}"
                )


# =========================================================
# DISPLAY PREDICTION
# =========================================================

if "prediction" in st.session_state:

    result = st.session_state["prediction"]

    prediction_date = result["prediction_date"]
    predicted_return = result["predicted_return"]
    signal = result["signal"]
    buy_threshold = result["buy_threshold"]
    sell_threshold = result["sell_threshold"]

    st.markdown("---")

    st.subheader(
        f"Prediction for {prediction_date}"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Predicted Return",
            f"{predicted_return * 100:.4f}%"
        )

    with col2:

        st.metric(
            "BUY Threshold",
            f"{buy_threshold * 100:.4f}%"
        )

    with col3:

        st.metric(
            "SELL Threshold",
            f"{sell_threshold * 100:.4f}%"
        )

    # Signal

    if signal == "BUY":

        st.success(
            "🟢 BUY SIGNAL"
        )

    elif signal == "SELL":

        st.error(
            "🔴 SELL SIGNAL"
        )

    else:

        st.warning(
            "🟡 HOLD SIGNAL"
        )

    # Explanation

    if signal == "BUY":

        st.info(
            "The predicted return is above the historical "
            "BUY threshold."
        )

    elif signal == "SELL":

        st.info(
            "The predicted return is below the historical "
            "SELL threshold."
        )

    else:

        st.info(
            "The predicted return is between the BUY and "
            "SELL thresholds."
        )


# =========================================================
# MARKET TREND
# =========================================================

st.markdown(
    '<div class="section-title">📈 Market Trend</div>',
    unsafe_allow_html=True
)

chart_df = df.tail(250)

fig, ax = plt.subplots(
    figsize=(14, 5)
)

ax.plot(
    chart_df["Date"],
    chart_df["Close"],
    linewidth=1.8
)

ax.set_title(
    "BankNifty Closing Price — Last 250 Trading Sessions",
    fontsize=14,
    fontweight="bold"
)

ax.set_xlabel("Date")
ax.set_ylabel("Close Price")

ax.grid(
    alpha=0.2
)

fig.autofmt_xdate()

st.pyplot(
    fig,
    use_container_width=True
)

plt.close(fig)


# =========================================================
# TECHNICAL INDICATORS
# =========================================================

st.markdown(
    '<div class="section-title">📊 Technical Indicators</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "SMA 50",
        f"{latest_row['SMA_50']:,.2f}"
    )

with col2:

    st.metric(
        "SMA 100",
        f"{latest_row['SMA_100']:,.2f}"
    )

with col3:

    st.metric(
        "MACD",
        f"{latest_row['MACD']:.4f}"
    )

with col4:

    st.metric(
        "Volatility 20D",
        f"{latest_row['Volatility_20']:.4f}"
    )


# =========================================================
# LATEST MARKET DATA
# =========================================================

st.markdown(
    '<div class="section-title">📋 Latest Market Data</div>',
    unsafe_allow_html=True
)

display_columns = [
    "Date",
    "Close",
    "High",
    "Low",
    "Open",
    "Volume",
    "RSI",
    "MACD",
    "Momentum"
]

available_columns = [
    col for col in display_columns
    if col in df.columns
]

latest_data = df[
    available_columns
].tail(20).copy()

st.dataframe(
    latest_data,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.caption(
    "BankNifty Signal Dashboard • "
    "Data powered by Yahoo Finance • "
    "Prediction powered by XGBoost"
)
