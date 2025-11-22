from utils.selenium_fetcher import fetch_live_price_selenium

print("Fetching Rajapalayam...")
data1 = fetch_live_price_selenium("Rajapalayam (Uzhavar Sandhai)")
print(data1)

print("\nFetching Thalavaipuram...")
data2 = fetch_live_price_selenium("Thalavaipuram (Uzhavar Sandhai)")
print(data2)
