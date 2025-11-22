import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import streamlit as st
import pandas as pd

# Market URLs
MARKET_URLS = {
    "Rajapalayam (Uzhavar Sandhai)": "https://www.commodityonline.com/mandiprices/lime/tamil-nadu/rajapalayam-uzhavar-sandhai",
    "Thalavaipuram (Uzhavar Sandhai)": "https://www.commodityonline.com/mandiprices/lime/tamil-nadu/thalavaipuram-uzhavar-sandhai"
}

@st.cache_resource
def get_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

@st.cache_data(ttl=3600)
def fetch_live_price_selenium(market_name):
    url = MARKET_URLS.get(market_name)
    if not url:
        return {"price": 0, "market": market_name, "date": "N/A", "error": "URL not found"}

    try:
        # We create a new driver instance for data fetching to avoid thread safety issues with caching the driver itself across requests if not careful.
        # But for performance, we can try to reuse. Streamlit's cache_resource handles the singleton.
        # However, for robustness in this script, let's just launch a fresh one or use the cached one carefully.
        # Let's use a fresh one for now to be safe against session timeouts.
        
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        # Try to find system chromium first (for Streamlit Cloud)
        try:
            service = Service("/usr/bin/chromedriver")
            options.binary_location = "/usr/bin/chromium"
            driver = webdriver.Chrome(service=service, options=options)
        except Exception:
            # Fallback to webdriver_manager (for local)
            service = Service(ChromeDriverManager().install())
            # Reset binary location if it was set above
            options.binary_location = "" 
            # Re-initialize options to be safe or just unset binary_location if possible. 
            # Easier to just re-create options or not set binary_location if falling back.
            # Let's simplify: if /usr/bin/chromium exists, use it.
            import os
            if os.path.exists("/usr/bin/chromium") and os.path.exists("/usr/bin/chromedriver"):
                 options.binary_location = "/usr/bin/chromium"
                 service = Service("/usr/bin/chromedriver")
                 driver = webdriver.Chrome(service=service, options=options)
            else:
                 # Local fallback
                 service = Service(ChromeDriverManager().install())
                 driver = webdriver.Chrome(service=service, options=options)
        
        try:
            driver.get(url)
            
            # Wait for the table to load
            wait = WebDriverWait(driver, 15)
            # Selector from inspection: div#table-scroll2 table tbody tr:first-child td:nth-child(9)
            price_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div#table-scroll2 table tbody tr:first-child td:nth-child(9)")))
            date_element = driver.find_element(By.CSS_SELECTOR, "div#table-scroll2 table tbody tr:first-child td:nth-child(2)")
            
            price_text = price_element.text.strip() # e.g. "Rs 21500 / Quintal"
            date_text = date_element.text.strip()   # e.g. "21/11/2025"
            
            # Parse price
            # Remove "Rs " and " / Quintal"
            clean_price = price_text.lower().replace("rs", "").replace("/ quintal", "").replace(",", "").strip()
            price_val = float(clean_price)
            
            return {
                "price": price_val,
                "market": market_name,
                "date": date_text
            }
            
        finally:
            driver.quit()
            
    except Exception as e:
        return {"price": 0, "market": market_name, "date": "N/A", "error": str(e)}
