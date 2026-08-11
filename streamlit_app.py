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
# API CONFIGURATION
# =========================================================

# Replace this with your actual Render API URL
API_URL = "https://bank-nifty-prediction.onrender.com/predict"


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    /* =====================================================
       MAIN APPLICATION
       ===================================================== */

    .stApp {
        background-color: #f8fafc;
    }

    .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }


    /* =====================================================
       SIDEBAR
       ===================================================== */

    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e2e8f0;
    }

    /* Force all sidebar text to dark */
    section[data-testid="stSidebar"] * {
        color: #1e293b !important;
    }

    /* Sidebar headings */
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] h4 {
        color: #0f172a !important;
    }

    /* Sidebar normal text */
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label {
        color: #334155 !important;
    }

    /* Sidebar captions */
    section[data-testid="stSidebar"] small {
        color: #64748b !important;
    }

    /* Sidebar warning */
    section[data-testid="stSidebar"]
    [data-testid="stAlert"] {
        background-color: #fffbeb !important;
        border-radius: 10px;
        border: 1px solid #fde68a;
    }

    section[data-testid="stSidebar"]
    [data-testid="stAlert"] * {
        color: #92400e !important;
    }


    /* =====================================================
       METRIC CARDS
       ===================================================== */

    [data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 18px;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.05);
    }

    [data-testid="stMetricLabel"] {
        color: #64748b !important;
    }

    [data-testid="stMetricValue"] {
        color: #0f172a !important;
        font-weight: 700;
    }


    /* =====================================================
       BUTTONS
       ===================================================== */

    .stButton > button {
        width: 100%;
        min-height: 48px;
        border-radius: 10px;
        border: none;
        background-color: #0f172a;
        color: white !important;
        font-weight: 600;
        font-size: 15px;
    }

    .stButton > button:hover {
        background-color: #1e293b;
        color: white !important;
    }


    /* =====================================================
       DATAFRAME
       ===================================================== */

    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
    }


    /* =====================================================
       FOOTER
       ===================================================== */

    .footer {
        text-align: center;
        color: #64748b;
        font-size: 13px;
        padding-top: 20px;
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

    st.error(
        f"Unable to load market data: {e}"
    )

    st.stop()


# =========================================================
# HEADER
# =========================================================

st.title("📈 BankNifty Prediction Dashboard")

st.caption(
    "Machine Learning powered market signal analysis "
    "using technical indicators and XGBoost."
)

st.divider()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("⚙️ Dashboard")

    st.divider()

    st.subheader("📊 Data Information")

    latest_date = df["Date"].max()

    st.write(
        f"**Latest Data:** "
        f"{latest_date.strftime('%d %b %Y')}"
    )

    st.write(
        f"**Total Records:** "
        f"{len(df):,}"
    )

    st.divider()

    st.subheader("🤖 Model Information")

    st.write("**Model:** XGBoost")

    st.write(
        "**Prediction:** Next Trading Day"
    )

    st.write(
        "**Signals:** BUY / HOLD / SELL"
    )

    st.divider()

    st.warning(
        "This dashboard is for educational and "
        "analytical purposes only."
    )


# =========================================================
# LATEST MARKET DATA
# =========================================================

latest_row = df.iloc[-1]

current_price = latest_row["Close"]

if len(df) > 1:

    previous_price = df.iloc[-2]["Close"]

else:

    previous_price = current_price


daily_change = (
    (current_price - previous_price)
    / previous_price
) * 100


# =========================================================
# MARKET OVERVIEW
# =========================================================

st.subheader("📊 Current Market Overview")

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

st.subheader("🤖 Next Trading Day Prediction")


if st.button(
    "🔮 Predict Next Trading Day",
    width="stretch"
):

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
                            "Prediction failed"
                        )
                    )

                except Exception:

                    error_message = (
                        f"Prediction API returned "
                        f"status code "
                        f"{response.status_code}"
                    )

                st.error(error_message)


        except requests.exceptions.Timeout:

            st.error(
                "Prediction API timed out. "
                "The free Render service may be "
                "starting up. Please try again."
            )


        except requests.exceptions.ConnectionError:

            st.error(
                "Could not connect to the prediction API. "
                "Please check that your Render service "
                "is running."
            )


        except requests.exceptions.RequestException as e:

            st.error(
                f"API request failed: {e}"
            )


# =========================================================
# DISPLAY PREDICTION
# =========================================================

if "prediction" in st.session_state:

    result = st.session_state["prediction"]

    prediction_date = result[
        "prediction_date"
    ]

    predicted_return = result[
        "predicted_return"
    ]

    signal = result[
        "signal"
    ]

    buy_threshold = result[
        "buy_threshold"
    ]

    sell_threshold = result[
        "sell_threshold"
    ]


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
    # Trading Signal
    # -----------------------------------------------------

    st.subheader("📌 Trading Signal")


    if signal == "BUY":

        st.success(
            "🟢 BUY SIGNAL"
        )

        st.info(
            "The predicted return is above the "
            "historical BUY threshold."
        )


    elif signal == "SELL":

        st.error(
            "🔴 SELL SIGNAL"
        )

        st.info(
            "The predicted return is below the "
            "historical SELL threshold."
        )


    else:

        st.warning(
            "🟡 HOLD SIGNAL"
        )

        st.info(
            "The predicted return is between the "
            "BUY and SELL thresholds."
        )


# =========================================================
# MARKET TREND
# =========================================================

st.subheader("📈 Market Trend")


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
    "BankNifty Closing Price — "
    "Last 250 Trading Sessions",
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
    width="stretch"
)


plt.close(fig)


# =========================================================
# TECHNICAL INDICATORS
# =========================================================

st.subheader("📊 Technical Indicators")


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
        "20D Volatility",
        f"{latest_row['Volatility_20']:.4f}"
    )


# =========================================================
# LATEST MARKET DATA TABLE
# =========================================================

st.subheader("📋 Latest Market Data")


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
    column
    for column in display_columns
    if column in df.columns
]


latest_data = (
    df[available_columns]
    .tail(20)
    .copy()
)


st.dataframe(
    latest_data,
    width="stretch",
    hide_index=True
)


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.markdown(
    """
    <div class="footer">
        BankNifty Signal Dashboard •
        Data powered by Yahoo Finance •
        Prediction powered by XGBoost
    </div>
    """,
    unsafe_allow_html=True
)
