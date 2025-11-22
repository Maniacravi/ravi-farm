import requests
from bs4 import BeautifulSoup

url = "https://www.commodityonline.com/mandiprices/lime/tamil-nadu/rajapalayam-uzhavar-sandhai"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

try:
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    print(f"Status Code: {response.status_code}")
    
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Selectors from browser subagent
    # Date: div#table-scroll2 table tbody tr:first-child td:nth-child(2)
    # Price: div#table-scroll2 table tbody tr:first-child td:nth-child(9)
    
    table = soup.select_one("div#table-scroll2 table tbody")
    if table:
        row = table.select_one("tr:first-child")
        if row:
            cols = row.find_all("td")
            if len(cols) >= 9:
                date_text = cols[1].get_text(strip=True)
                price_text = cols[8].get_text(strip=True)
                print(f"Date: {date_text}")
                print(f"Price: {price_text}")
            else:
                print("Row found but not enough columns")
        else:
            print("Table found but no rows")
    else:
        print("Table not found")

except Exception as e:
    print(f"Error: {e}")
