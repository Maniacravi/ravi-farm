import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

st.title("Ravi Farm - Lime Prices and Weather Data")
st.write(" Welcome to Ravi Farm's data dashboard! Here you can explore lime prices and weather data.")

def fetch_lime_prices(district = 'virudhunagar', market = 'rajapalayam-uzhavar-sandhai'):
    url = 'https://www.agriplus.in/price/lime/tamil-nadu/{}/{}'.format(district, market)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    prices = []
    table = soup.find('table')
    if table:
        rows = table.find_all('tr')
        for row in rows[1:]:
            cols = row.find_all('td')
            if len(cols) >= 2:
                date = cols[0].text.strip()
                # convert date to standard format if needed from '6 Nov' to '2025-11-06' where 2025 is current year
                date = datetime.strptime(date + ' ' + str(datetime.now().year), '%d %b %Y').date()
                variety = cols[1].text.strip()
                min_price = cols[2].text.strip()
                max_price = cols[3].text.strip()
                modal_price = cols[4].text.strip()
                prices.append({'date': date, 'market': market, 'variety': variety, 'min_price': min_price, 'max_price': max_price, 'modal_price': modal_price})
    return prices

markets = ['rajapalayam-uzhavar-sandhai', 'thalavaipuram-uzhavar-sandhai', 'aruppukottai-uzhavar-sandhai']
all_prices = []
# Go through markets and get prices
for market in markets:
    price = fetch_lime_prices(market=market)
    all_prices.extend(price)
df_prices = pd.DataFrame(all_prices)

st.subheader("Lime Prices in Virudhunagar District")
st.dataframe(df_prices)
st.line_chart(df_prices.set_index('date')[['modal_price']])
st.write("Data sourced from Agriplus.in")
st.write("Developed by Manikandan Ravi - ravi.farm")
