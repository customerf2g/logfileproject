
import yfinance as yf
import streamlit as st
import plotly.graph_objects as go 

st.set_page_config(page_title="Stock Candlestick Chart", layout="wide")

st.title("Stock Price Candlestick App")

ticker_symbol = st.text_input("Enter stock ticker", "GOOGL").upper()

period = st.selectbox(
    "Select historical period",
    ["1mo", "3mo", "6mo", "1y", "2y", "5y"],
    index=0
)

if st.button("Load Chart"):
    with st.spinner("Loading stock data..."):
        ticker_data = yf.Ticker(ticker_symbol)
        ticker_df = ticker_data.history(period=period)

    if ticker_df.empty:
        st.error("No data found. Check the ticker symbol.")
    else:
        # Candlestick chart
        fig = go.Figure(
            data=[
                go.Candlestick(
                    x=ticker_df.index,
                    open=ticker_df["Open"],
                    high=ticker_df["High"],
                    low=ticker_df["Low"],
                    close=ticker_df["Close"],
                    name=ticker_symbol
                )
            ]
        )

        fig.update_layout(
            title=f"{ticker_symbol} Candlestick Chart",
            xaxis_title="Date",
            yaxis_title="Price (USD)",
            xaxis_rangeslider_visible=False,
            height=600
        )

        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Trading Volume")
        st.bar_chart(ticker_df["Volume"])

        st.subheader("Historical Data")
        st.dataframe(ticker_df)
