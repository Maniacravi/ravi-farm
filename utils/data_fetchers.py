import requests, pandas as pd
from datetime import datetime, timedelta
import streamlit as st

@st.cache_data(ttl=86400)
def fetch_live_price():
    url = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
    params = {
        "api-key": st.secrets["DATA_GOV_API_KEY"],
        "format": "json",
        "filters[state]": "Tamil Nadu",
        "filters[market]": "Rajapalayam (Uzhavar Sandhai)",
        "filters[commodity]": "Lemon",
        "limit": 1,
        "sort[date]": "-1"
    }
    try:
        r = requests.get(url, params=params)
        data = r.json()["records"][0]
        return {
            "price": float(data["modal_price"]),
            "market": data["market"],
            "date": data["arrival_date"]
        }
    except Exception:
        return {"price": 20000, "market": "Rajapalayam (Mock)", "date": "N/A"}

@st.cache_data(ttl=86400)
def fetch_history(days=180):
    today = datetime.now()
    data = []
    v = 12000
    for i in range(days):
        d = today - timedelta(days=days - i)
        v *= 0.995 + 0.01*(i%7==0)
        data.append({"date": d.date(), "modal": v})
    return pd.DataFrame(data)

@st.cache_data(ttl=3600)
def fetch_weather():
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat=9.4511&lon=77.5536&appid={st.secrets['OPENWEATHER_API_KEY']}&units=metric"
        r = requests.get(url)
        j = r.json()
        rain = j.get('rain', {}).get('1h', 0)
        return {
            "temp": j['main']['temp'],
            "rain": rain,
            "humidity": j['main']['humidity'],
            "rainfall": [{"date": (datetime.now() - timedelta(days=i)).date(), "rain": 5*abs((i%5 - 2))} for i in range(6,-1,-1)]
        }
    except Exception:
        return {"temp": 30.5, "rain": 1.2, "humidity": 70, "rainfall": [{"date": (datetime.now() - timedelta(days=i)).date(), "rain": 2.0} for i in range(6,-1,-1)]}
