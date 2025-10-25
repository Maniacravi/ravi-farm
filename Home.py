import streamlit as st
import pandas as pd
from utils.data_fetchers import fetch_live_price, fetch_history, fetch_weather
from utils.forecast_utils import forecast_next, monthly_forecast

st.set_page_config(page_title="Ravi Farm Dashboard", page_icon="🌿", layout="wide")

st.title("🌿 Ravi Farm Dashboard")
st.markdown("Live **lime prices**, **forecasts**, and **weather** – Rajapalayam, Tamil Nadu")

live = fetch_live_price()
history = fetch_history(days=180)
weather = fetch_weather()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Live Lime Price", f"₹{live['price']:,}/Qtl", help=live['market'])
col2.metric("7-Day Forecast", "₹" + f"{forecast_next(history['modal'], 7)[-1]:,.0f}")
col3.metric("12-Month Outlook", "₹" + f"{monthly_forecast(history['modal'])[-1]:,.0f}")
col4.metric("Temp / Rain", f"{weather['temp']}°C / {weather['rain']} mm")

st.subheader("📈 Daily Lime Prices (₹/Qtl)")
st.line_chart(history.set_index("date")["modal"])

st.subheader("🌦️ 7-Day Rainfall Trend (mm)")
rain_df = pd.DataFrame(weather["rainfall"])
st.area_chart(rain_df.set_index("date")["rain"])

st.caption("Data: AGMARKNET, OpenWeatherMap, IMD datasets. Forecasts are for planning only.")
