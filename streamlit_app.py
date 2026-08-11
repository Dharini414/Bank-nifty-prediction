import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="BankNifty Prediction Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# API CONFIGURATION
# =========================================================

# IMPORTANT:
# Replace this with your actual Render Flask API URL.

API_URL = "https://bank-nifty-prediction.onrender.com/predict"


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    /* =====================================================
       GLOBAL
       ===================================================== */

    html,
    body,
    [class*="css"] {
        font-family: Arial, sans-serif;
    }

    .stApp {
        background-color: #f8fafc !important;
        color: #0f172a !important;
    }

    .main {
        background-color: #f8fafc !important;
    }

    .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }


    /* =====================================================
       MAIN TEXT
       ===================================================== */

    .main h1,
    .main h2,
    .main h3,
    .main h4 {
        color: #0f172a !important;
    }

    .main p {
        color: #334155 !important;
    }

    .main li {
        color: #334155 !important;
    }

    .main label {
        color: #334155 !important;
    }

    [data-testid="stTitle"] {
        color: #0f172a !important;
    }

    [data-testid="stTitle"] * {
        color: #0f172a !important;
    }

    [data-testid="stCaptionContainer"] {
        color: #64748b !important;
    }

    [data-testid="stCaptionContainer"] * {
        color: #64748b !important;
    }

    .stMarkdown p {
        color: #334155 !important;
    }

    .stMarkdown strong {
        color: #0f172a !important;
    }


    /* =====================================================
       SIDEBAR
       ===================================================== */

    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e2e8f0 !important;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] h4 {
        color: #0f172a !important;
    }

    section[data-testid="stSidebar"] p {
        color: #334155 !important;
    }

    section[data-testid="stSidebar"] span {
        color: #334155 !important;
    }

    section[data-testid="stSidebar"] label {
        color: #334155 !important;
    }

    section[data-testid="stSidebar"] small {
        color: #64748b !important;
    }

    section[data-testid="stSidebar"] .stMarkdown p {
        color: #334155 !important;
    }

    section[data-testid="stSidebar"] .stMarkdown strong {
        color: #0f172a !important;
    }


    /* =====================================================
       METRIC CARDS
       ===================================================== */

    [data-testid="stMetric"] {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 14px !important;
        padding: 18px !important;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.05);
    }

    [data-testid="stMetricLabel"] {
        color: #64748b !important;
    }

    [data-testid="stMetricLabel"] * {
        color: #64748b !important;
    }

    [data-testid="stMetricValue"] {
        color: #0f172a !important;
        font-weight: 700 !important;
    }

    [data-testid="stMetricValue"] * {
        color: #0f172a !important;
    }

    [data-testid="stMetricDelta"] {
        color: #475569 !important;
    }

    [data-testid="stMetricDelta"] * {
        color: #475569 !important;
    }


    /* =====================================================
       PREDICTION BUTTON
       ===================================================== */

    .stButton > button {
        width: 100%;
        min-height: 50px;

        background-color: #0f172a !important;

        border: none !important;
        border-radius: 10px !important;

        color: #ffffff !important;

        font-size: 15px !important;
        font-weight: 600 !important;
    }

    .stButton > button p {
        color: #ffffff !important;
    }

    .stButton > button span {
        color: #ffffff !important;
    }

    .stButton > button:hover {
        background-color: #1e293b !important;
        color: #ffffff !important;
    }

    .stButton > button:hover p,
    .stButton > button:hover span {
        color: #ffffff !important;
    }


    /* =====================================================
       CUSTOM SIGNAL CARDS
       ===================================================== */

    .signal-card {
        width: 100%;
        padding: 22px;
        margin-top: 10px;
        margin-bottom: 15px;

        border-radius: 14px;

        text-align: center;

        box-sizing: border-box;
    }

    .signal-card h2 {
        margin: 0 0 8px 0;
        font-size: 26px;
        font-weight: 700;
    }

    .signal-card p {
        margin: 0;
        font-size: 15px;
    }


    /* BUY */

    .buy-card {
        background-color: #ecfdf5;
        border: 1px solid #86efac;
    }

    .buy-card h2 {
        color: #166534 !important;
    }

    .buy-card p {
        color: #166534 !important;
    }


    /* SELL */

    .sell-card {
        background-color: #fef2f2;
        border: 1px solid #fca5a5;
    }

    .sell-card h2 {
        color: #991b1b !important;
    }

    .sell-card p {
        color: #991b1b !important;
    }


    /* HOLD */

    .hold-card {
        background-color: #fffbeb;
        border: 1px solid #fcd34d;
    }

    .hold-card h2 {
        color: #92400e !important;
    }

    .hold-card p {
        color: #92400e !important;
    }


    /* =====================================================
       INFORMATION CARD
       ===================================================== */

    .info-card {
        background-color: #eff6ff;
        border: 1px solid #bfdbfe;

        border-radius: 12px;

        padding: 16px 18px;

        margin-top: 8px;
        margin-bottom: 18px;
    }

    .info-card p {
        color: #1e40af !important;
        margin: 0;
        font-size: 14px;
    }


    /* =====================================================
       ERROR CARD
       ===================================================== */

    .error-card {
        background-color: #fef2f2;
        border: 1px solid #fca5a5;

        border-radius: 12px;

        padding: 16px 18px;

        margin-top: 10px;
        margin-bottom: 18px;
    }

    .error-card p {
        color: #991b1b !important;
        margin: 0;
        font-size: 14px;
    }


    /* =====================================================
       SIDEBAR DISCLAIMER
       ===================================================== */

    .sidebar-warning {
        background-color: #fffbeb;

        border: 1px solid #fde68a;

        border-radius: 10px;

        padding: 12px;

        margin-top: 10px;
    }

    .sidebar-warning p {
        color: #92400e !important;

        font-size: 13px;

        margin: 0;

        line-height: 1.5;
    }


    /* =====================================================
       FOOTER
       ===================================================== */

    .footer {
        text-align: center;

        color: #64748b !important;

        font-size: 13px;

        padding-top: 20px;
    }

    .footer p {
        color: #64748b !important;
    }


    /* =====================================================
       DIVIDERS
       ===================================================== */

    hr {
        border-color: #e2e8f0 !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data(ttl=3600)
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

    st.markdown(
        f"""
        <div class="error-card">
            <p>
                <strong>Unable to load market data.</strong><br>
                {str(e)}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.stop()


# =========================================================
# CHECK REQUIRED COLUMNS
# =========================================================

required_columns = [
    "Date",
    "Close",
    "RSI",
    "Momentum",
    "Price_vs_SMA50",
    "SMA_50",
    "SMA_100",
    "MACD",
    "Volatility_20"
]


missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]


if missing_columns:

    st.markdown(
        f"""
        <div class="error-card">
            <p>
                <strong>Missing required columns:</strong><br>
                {", ".join(missing_columns)}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.stop()


# =========================================================
# HEADER
# =========================================================

st.title(
    "📈 BankNifty Prediction Dashboard"
)

st.caption(
    "Machine Learning powered market analysis using "
    "technical indicators and an XGBoost prediction model."
)

st.divider()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("⚙️ Dashboard")

    st.divider()

    st.subheader("📊 Market Data")

    latest_date = df["Date"].max()

    st.write(
        f"**Latest Data:** "
        f"{latest_date.strftime('%d %b %Y')}"
    )

    st.write(
        f"**Trading Sessions:** "
        f"{len(df):,}"
    )

    st.divider()

    st.subheader("🤖 Model")

    st.write(
        "**Algorithm:** XGBoost"
    )

    st.write(
        "**Target:** Future Return"
    )

    st.write(
        "**Forecast:** Next Trading Day"
    )

    st.divider()

    st.subheader("📌 Signal Logic")

    st.write(
        "**BUY:** ≥ 90th percentile"
    )

    st.write(
        "**SELL:** ≤ 10th percentile"
    )

    st.write(
        "**HOLD:** Between thresholds"
    )

    st.divider()

    st.markdown(
        """
        <div class="sidebar-warning">
            <p>
                ⚠️ This dashboard is for educational
                and analytical purposes only.
                It is not financial advice.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# LATEST MARKET VALUES
# =========================================================

latest_row = df.iloc[-1]

current_price = float(
    latest_row["Close"]
)


if len(df) > 1:

    previous_price = float(
        df.iloc[-2]["Close"]
    )

else:

    previous_price = current_price


daily_change = (
    (current_price - previous_price)
    / previous_price
) * 100


# =========================================================
# MARKET OVERVIEW
# =========================================================

st.subheader(
    "📊 Market Overview"
)

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
        f"{float(latest_row['RSI']):.2f}"
    )


with col3:

    st.metric(
        "Momentum",
        f"{float(latest_row['Momentum']):,.2f}"
    )


with col4:

    st.metric(
        "Price / SMA50",
        f"{float(latest_row['Price_vs_SMA50']):.3f}"
    )


# =========================================================
# PREDICTION SECTION
# =========================================================

st.subheader(
    "🤖 Next Trading Day Prediction"
)


predict_clicked = st.button(
    "🔮 Predict Next Trading Day",
    width="stretch"
)


# =========================================================
# API REQUEST
# =========================================================

if predict_clicked:

    with st.spinner(
        "Connecting to prediction model..."
    ):

        try:

            response = requests.get(
                API_URL,
                timeout=120
            )


            if response.status_code == 200:

                result = response.json()

                st.session_state[
                    "prediction"
                ] = result


            else:

                try:

                    error_message = (
                        response.json().get(
                            "error",
                            "Prediction failed."
                        )
                    )

                except Exception:

                    error_message = (
                        "Prediction API returned "
                        f"HTTP {response.status_code}."
                    )


                st.markdown(
                    f"""
                    <div class="error-card">
                        <p>
                            <strong>Prediction failed.</strong><br>
                            {error_message}
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )


        except requests.exceptions.Timeout:

            st.markdown(
                """
                <div class="error-card">
                    <p>
                        <strong>Prediction API timed out.</strong><br>
                        The free Render service may be waking up.
                        Please wait a few seconds and try again.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )


        except requests.exceptions.ConnectionError:

            st.markdown(
                """
                <div class="error-card">
                    <p>
                        <strong>Could not connect to the API.</strong><br>
                        Please check that your Render Flask
                        service is running.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )


        except requests.exceptions.RequestException as e:

            st.markdown(
                f"""
                <div class="error-card">
                    <p>
                        <strong>API request failed.</strong><br>
                        {str(e)}
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )


        except Exception as e:

            st.markdown(
                f"""
                <div class="error-card">
                    <p>
                        <strong>Unexpected error.</strong><br>
                        {str(e)}
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )


# =========================================================
# DISPLAY PREDICTION
# =========================================================

if "prediction" in st.session_state:

    result = st.session_state["prediction"]


    # -----------------------------------------------------
    # Safely read API response
    # -----------------------------------------------------

    prediction_date = result.get(
        "prediction_date",
        "Unknown"
    )

    predicted_return = float(
        result.get(
            "predicted_return",
            0
        )
    )

    signal = str(
        result.get(
            "signal",
            "HOLD"
        )
    ).upper()

    buy_threshold = float(
        result.get(
            "buy_threshold",
            0
        )
    )

    sell_threshold = float(
        result.get(
            "sell_threshold",
            0
        )
    )


    # -----------------------------------------------------
    # Prediction heading
    # -----------------------------------------------------

    st.divider()

    st.subheader(
        f"🎯 Prediction for {prediction_date}"
    )


    # -----------------------------------------------------
    # Prediction metrics
    # -----------------------------------------------------

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


    # -----------------------------------------------------
    # Signal
    # -----------------------------------------------------

    st.subheader(
        "📌 Trading Signal"
    )


    if signal == "BUY":

        st.markdown(
            """
            <div class="signal-card buy-card">
                <h2>🟢 BUY SIGNAL</h2>
                <p>
                    The predicted return is above the
                    historical BUY threshold.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )


    elif signal == "SELL":

        st.markdown(
            """
            <div class="signal-card sell-card">
                <h2>🔴 SELL SIGNAL</h2>
                <p>
                    The predicted return is below the
                    historical SELL threshold.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )


    else:

        st.markdown(
            """
            <div class="signal-card hold-card">
                <h2>🟡 HOLD SIGNAL</h2>
                <p>
                    The predicted return is between the
                    BUY and SELL thresholds.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )


    # -----------------------------------------------------
    # Prediction explanation
    # -----------------------------------------------------

    st.markdown(
        f"""
        <div class="info-card">
            <p>
                <strong>Prediction:</strong>
                {predicted_return * 100:.4f}% &nbsp; • &nbsp;

                <strong>BUY threshold:</strong>
                {buy_threshold * 100:.4f}% &nbsp; • &nbsp;

                <strong>SELL threshold:</strong>
                {sell_threshold * 100:.4f}%
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# BANKNIFTY PRICE CHART
# =========================================================

st.subheader(
    "📈 BankNifty Price Trend"
)


chart_df = df.tail(250)


fig, ax = plt.subplots(
    figsize=(14, 5)
)


ax.plot(
    chart_df["Date"],
    chart_df["Close"],
    linewidth=2
)


ax.set_title(
    "BankNifty Closing Price — Last 250 Trading Sessions",
    fontsize=14,
    fontweight="bold"
)

ax.set_xlabel("Date")

ax.set_ylabel("BankNifty")

ax.grid(
    alpha=0.2
)


fig.autofmt_xdate()


st.pyplot(
    fig,
    width="stretch"
)


plt.close(fig)


# =========================================================
# RSI CHART
# =========================================================

st.subheader(
    "📊 RSI Trend"
)


rsi_df = df.tail(150)


fig, ax = plt.subplots(
    figsize=(14, 4)
)


ax.plot(
    rsi_df["Date"],
    rsi_df["RSI"],
    linewidth=1.8
)


ax.axhline(
    70,
    linestyle="--",
    linewidth=1
)


ax.axhline(
    30,
    linestyle="--",
    linewidth=1
)


ax.set_title(
    "Relative Strength Index (RSI)",
    fontsize=14,
    fontweight="bold"
)

ax.set_xlabel("Date")

ax.set_ylabel("RSI")

ax.set_ylim(
    0,
    100
)

ax.grid(
    alpha=0.2
)


fig.autofmt_xdate()


st.pyplot(
    fig,
    width="stretch"
)


plt.close(fig)


# =========================================================
# MOVING AVERAGE CHART
# =========================================================

st.subheader(
    "📉 Moving Average Trend"
)


ma_df = df.tail(250)


fig, ax = plt.subplots(
    figsize=(14, 5)
)


ax.plot(
    ma_df["Date"],
    ma_df["Close"],
    linewidth=1.8,
    label="BankNifty"
)


ax.plot(
    ma_df["Date"],
    ma_df["SMA_50"],
    linewidth=1.4,
    label="SMA 50"
)


ax.plot(
    ma_df["Date"],
    ma_df["SMA_100"],
    linewidth=1.4,
    label="SMA 100"
)


ax.set_title(
    "BankNifty vs Moving Averages",
    fontsize=14,
    fontweight="bold"
)

ax.set_xlabel("Date")

ax.set_ylabel("Price")

ax.legend()

ax.grid(
    alpha=0.2
)


fig.autofmt_xdate()


st.pyplot(
    fig,
    width="stretch"
)


plt.close(fig)


# =========================================================
# TECHNICAL INDICATORS
# =========================================================

st.subheader(
    "📊 Technical Indicators"
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "SMA 50",
        f"{float(latest_row['SMA_50']):,.2f}"
    )


with col2:

    st.metric(
        "SMA 100",
        f"{float(latest_row['SMA_100']):,.2f}"
    )


with col3:

    st.metric(
        "MACD",
        f"{float(latest_row['MACD']):.4f}"
    )


with col4:

    st.metric(
        "20D Volatility",
        f"{float(latest_row['Volatility_20']):.4f}"
    )


# =========================================================
# MARKET INTERPRETATION
# =========================================================

st.subheader(
    "🔎 Market Interpretation"
)


summary_col1, summary_col2 = st.columns(2)


with summary_col1:

    rsi_value = float(
        latest_row["RSI"]
    )


    if rsi_value >= 70:

        st.markdown(
            """
            <div class="signal-card sell-card">
                <h2>⚠️ RSI: Overbought</h2>
                <p>
                    RSI is above 70, indicating
                    relatively strong upward momentum.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )


    elif rsi_value <= 30:

        st.markdown(
            """
            <div class="signal-card buy-card">
                <h2>📉 RSI: Oversold</h2>
                <p>
                    RSI is below 30, indicating
                    relatively weak recent momentum.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )


    else:

        st.markdown(
            """
            <div class="signal-card hold-card">
                <h2>⚖️ RSI: Neutral</h2>
                <p>
                    RSI is currently between the
                    traditional 30 and 70 levels.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )


with summary_col2:

    price_vs_sma = float(
        latest_row["Price_vs_SMA50"]
    )


    if price_vs_sma > 1:

        st.markdown(
            """
            <div class="signal-card buy-card">
                <h2>📈 Above SMA 50</h2>
                <p>
                    BankNifty is currently trading
                    above its 50-day moving average.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )


    else:

        st.markdown(
            """
            <div class="signal-card sell-card">
                <h2>📉 Below SMA 50</h2>
                <p>
                    BankNifty is currently trading
                    below its 50-day moving average.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.markdown(
    """
    <div class="footer">
        <p>
            BankNifty Prediction Dashboard
            • XGBoost Machine Learning Model
            • Technical Indicator Analysis
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
