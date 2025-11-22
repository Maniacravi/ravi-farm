import requests, pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
import streamlit as st

DATA_DIR = Path("data")
HISTORY_FILE = DATA_DIR / "lime_prices.csv"
AGMARK_RESOURCE_ID = "9ef84268-d588-465a-a308-a864a43d0070"
AGMARK_URL = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
TARGET_STATE = "Tamil Nadu"
TARGET_MARKET = "Rajapalayam (Uzhavar Sandhai)"
TARGET_COMMODITY = "Lemon"
AGMARK_FILTER_VARIANTS = [
    {
        "filters[state]": TARGET_STATE,
        "filters[market]": TARGET_MARKET,
        "filters[commodity]": TARGET_COMMODITY,
    },
    {
        "filters[state]": TARGET_STATE,
        "filters[commodity]": TARGET_COMMODITY,
    },
    {
        "filters[commodity]": TARGET_COMMODITY,
    },
    {},
]


def _get_api_key():
    try:
        return st.secrets.get("DATA_GOV_API_KEY")
    except (FileNotFoundError, KeyError):
        return None


def _request_agmark_data(limit=10, offset=0, filters=None):
    key = _get_api_key()
    if not key:
        raise KeyError("DATA_GOV_API_KEY missing in secrets")

    params = {
        "api-key": key,
        "limit": limit,
        "offset": offset,
        "format": "json",
        "resource_id": AGMARK_RESOURCE_ID,
        "sort[date]": "-1",
    }
    if filters:
        params.update(filters)
    response = requests.get(AGMARK_URL, params=params, timeout=10)
    response.raise_for_status()
    payload = response.json()
    if payload.get("status") == "error":
        raise ValueError(payload.get("message", "Unknown API error"))
    return payload.get("records", [])


@st.cache_data(ttl=86400)
def fetch_live_price(target_market=TARGET_MARKET):
    try:
        last_error = None
        # Create filters specific to the target market
        market_filters = [
            {
                "filters[state]": TARGET_STATE,
                "filters[market]": target_market,
                "filters[commodity]": TARGET_COMMODITY,
            },
            # Fallback to state/commodity if market specific fails (though we might want to be strict)
            {
                "filters[state]": TARGET_STATE,
                "filters[commodity]": TARGET_COMMODITY,
            },
        ]

        for filters in market_filters:
            try:
                records = _request_agmark_data(limit=10, filters=filters)
            except ValueError as err:
                last_error = str(err)
                continue

            if not records:
                continue

            if "filters[market]" in filters:
                market_records = records
            else:
                market_records = [
                    r for r in records if r.get("market") == target_market
                ]

            if not market_records:
                continue

            data = market_records[0]
            return {
                "price": float(data["modal_price"]),
                "market": data["market"],
                "date": data["arrival_date"],
            }

        if last_error:
            st.info(f"Live price API fallback in use for {target_market} ({last_error}).")
    except Exception as exc:
        if isinstance(exc, KeyError):
            st.warning("Add DATA_GOV_API_KEY to Streamlit secrets for live pricing.")
        return {"price": 20000, "market": f"{target_market} (Mock)", "date": "N/A"}

@st.cache_data(ttl=86400)
def fetch_history(days=180):
    # Try live history via API (paged, 10 records per request for trial keys)
    try:
        limit = 10
        max_records = max(days, 30) if days else 180
        last_error = None
        api_records = None

        used_broader_data = False
        for filters in AGMARK_FILTER_VARIANTS:
            collected = []
            offset = 0
            while len(collected) < max_records:
                try:
                    page = _request_agmark_data(limit=limit, offset=offset, filters=filters)
                except ValueError as err:
                    last_error = str(err)
                    break

                if not page:
                    break

                if "filters[market]" in filters:
                    filtered_page = page
                else:
                    filtered_page = [r for r in page if r.get("market") == TARGET_MARKET]

                if not filtered_page and "filters[market]" not in filters:
                    # Fall back to using the raw page after a few attempts
                    filtered_page = page
                    used_broader_data = True

                collected.extend(filtered_page)
                offset += limit

                if len(page) < limit:
                    break

            if collected:
                api_records = collected
                break

        if api_records:
            df_api = pd.DataFrame(api_records)
            df_api["date"] = pd.to_datetime(df_api["arrival_date"]).dt.date
            df_api["modal"] = pd.to_numeric(df_api["modal_price"], errors="coerce")
            df_api = df_api.dropna(subset=["modal"])
            df_api = df_api.sort_values("date")
            if days:
                latest = df_api["date"].max()
                if pd.notna(latest):
                    cutoff = latest - timedelta(days=days - 1)
                    df_api = df_api[df_api["date"] >= cutoff]
            if not df_api.empty:
                if used_broader_data:
                    st.info("Showing latest AGMARKNET lemon prices; Rajapalayam entries not found in the API window.")
                return df_api[["date", "modal"]].reset_index(drop=True)

        if last_error:
            # st.info(f"Historical API fallback in use ({last_error}).") # Suppress fallback info
            pass
    except Exception as exc:
        if isinstance(exc, KeyError):
            # st.info("Provide DATA_GOV_API_KEY to load historic prices from AGMARKNET.") # Suppress missing key info
            pass
        else:
            st.warning(f"Could not load historic prices from API ({exc}).")

    # Then try user-supplied CSV
    try:
        if HISTORY_FILE.exists():
            df = pd.read_csv(HISTORY_FILE)
            if "date" not in df.columns or "modal" not in df.columns:
                raise ValueError("CSV must contain 'date' and 'modal' columns")
            df = df.copy()
            df["date"] = pd.to_datetime(df["date"]).dt.date
            df["modal"] = pd.to_numeric(df["modal"], errors="coerce")
            df = df.dropna(subset=["modal"])
            df = df.sort_values("date")
            if days:
                latest = df["date"].max()
                if pd.notna(latest):
                    cutoff = latest - timedelta(days=days - 1)
                    df = df[df["date"] >= cutoff]
            return df[["date", "modal"]].reset_index(drop=True)
    except Exception as exc:
        st.warning(f"Historical price CSV could not be used ({exc}). Showing simulated data.")

    today = datetime.now()
    data = []
    v = 12000
    for i in range(days):
        d = today - timedelta(days=days - i)
        v *= 0.995 + 0.01 * (i % 7 == 0)
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
