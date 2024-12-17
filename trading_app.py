import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(page_title="Trading Practice Platform", layout="wide")

def get_stock_data(symbol, bars=262):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=bars * 2)
    df = yf.download(symbol, start=start_date, end=end_date)
    return df.tail(bars)

def create_chart(data, hide_last_n=10, reveal=False):
    visible_data = data[:-hide_last_n] if not reveal else data

    fig = go.Figure(data=[go.Candlestick(x=visible_data.index,
                                        open=visible_data['Open'],
                                        high=visible_data['High'],
                                        low=visible_data['Low'],
                                        close=visible_data['Close'])])

    fig.update_layout(
        title="Stock Price Chart",
        yaxis_title="Price",
        xaxis_title="Date",
        height=600,
        template="plotly_dark"
    )
    return fig

# Initialize session state
if 'revealed' not in st.session_state:
    st.session_state.revealed = False
if 'correct_prediction' not in st.session_state:
    st.session_state.correct_prediction = None

st.title("Trading Practice Platform")

# Stock symbol input
symbol = st.text_input("Enter Stock Symbol (e.g., AAPL):", "AAPL")

try:
    # Get data
    data = get_stock_data(symbol)

    # Calculate if last 10 bars were bullish or bearish
    last_10_bars = data[-10:]
    actual_movement = "Bullish" if last_10_bars['Close'].iloc[-1] > last_10_bars['Open'].iloc[0] else "Bearish"

    # Create chart
    chart = create_chart(data, hide_last_n=10, reveal=st.session_state.revealed)
    st.plotly_chart(chart, use_container_width=True)

    # Buttons in columns
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Bullish", disabled=st.session_state.revealed):
            st.session_state.revealed = True
            st.session_state.correct_prediction = (actual_movement == "Bullish")
            st.experimental_rerun()

    with col2:
        if st.button("Bearish", disabled=st.session_state.revealed):
            st.session_state.revealed = True
            st.session_state.correct_prediction = (actual_movement == "Bearish")
            st.experimental_rerun()

    # Show result after prediction
    if st.session_state.revealed:
        if st.session_state.correct_prediction:
            st.success("Correct! The market was " + actual_movement)
        else:
            st.error("Wrong! The market was " + actual_movement)

        if st.button("Try Again"):
            st.session_state.revealed = False
            st.session_state.correct_prediction = None
            st.experimental_rerun()

except Exception as e:
    st.error(f"Error: {str(e)}")
