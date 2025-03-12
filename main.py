import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import yfinance as yf


def get_stock_data(ticker):
    stock = yf.Ticker(ticker)

    company_name = stock.info.get("longName", "N/A")  # Company Name
    last_price = stock.history(period="1d")["Close"].iloc[-1]  # Last stock price
    eps_ttm = stock.info.get("trailingEps", "N/A")  # EPS TTM
    pe_ratio = stock.info.get("trailingPE", "N/A")  # PE Ratio
    eps_growth = stock.info.get("earningsGrowth", "N/A")  # EPS Growth Rate

    return {
        "Company Name": company_name,
        "Last Price": last_price,
        "EPS (TTM)": eps_ttm,
        "PE Ratio": pe_ratio,
        "EPS Growth Rate": eps_growth
    }

# Streamlit UI
st.title("Stock Valuation & 5-Year Projection")

st.sidebar.header("Stock Selection")
ticker = st.sidebar.text_input("Enter Stock Ticker:", "AAPL")  # Default: Apple
stock_data = get_stock_data(ticker)

st.sidebar.write(f"### {stock_data['Company Name']}")
st.sidebar.write(f"**Last Price:** ${stock_data['Last Price']:.2f}")
st.sidebar.write(f"**EPS (TTM):** {stock_data['EPS (TTM)']}")
st.sidebar.write(f"**PE Ratio:** {stock_data['PE Ratio']}")
st.sidebar.write(f"**EPS Growth Rate:** {stock_data['EPS Growth Rate'] * 100:.2f}%")


st.sidebar.header("Assumptions")
eps_ttm = st.sidebar.number_input("EPS (TTM)", min_value=0.1, value=8.00)
eps_growth_rate = st.sidebar.number_input("EPS Growth Rate (%)", min_value=0.1, value=10.0)
pe_ratio = st.sidebar.number_input("Appropriate EPS Multiple (P/E)", min_value=1, value=19)
desired_return = st.sidebar.number_input("Desired Return (%)", min_value=0.1, value=15.0)

# Calculate Future EPS & Stock Price
years = np.arange(1, 6)
future_eps = [eps_ttm * ((1 + eps_growth_rate / 100) ** year) for year in years]
future_prices = [eps * pe_ratio for eps in future_eps]

# Calculate Required Entry Price
future_value = future_prices[-1]  # Stock price at year 5
entry_price = future_value / ((1 + desired_return / 100) ** 5)

# Display Results
st.metric(label="Entry Price for 15% Return", value=f"${entry_price:.2f}")

# Graph Data
df = pd.DataFrame({"Year": years, "Projected Stock Price": future_prices})
fig = px.line(df, x="Year", y="Projected Stock Price", markers=True, title="5-Year Stock Projection")
fig.update_yaxes(range=[0, max(future_prices) * 1.1])

# Display Graph
st.plotly_chart(fig)
