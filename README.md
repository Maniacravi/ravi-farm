# Ravi Farm Dashboard 🌿

A Streamlit-based dashboard for Ravi Farm in Rajapalayam, Tamil Nadu. This application tracks live lime prices, provides price forecasts, and monitors local weather conditions to aid in farming decisions.

## Features
- **Live Lime Prices**: Fetches real-time modal prices from AGMARKNET for the Rajapalayam market.
- **Price Forecasting**: Uses exponential smoothing to forecast prices for the next 7 days and provides a 12-month outlook.
- **Weather Monitoring**: Displays current temperature, rainfall, and humidity using OpenWeatherMap API.
- **Interactive Charts**: Visualizes historical price trends and rainfall data.

## Setup & Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd ravi-farm
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Secrets:**
    Create a `.streamlit/secrets.toml` file in the root directory (or configure secrets in Streamlit Cloud) with the following keys:
    ```toml
    DATA_GOV_API_KEY = "your_agmarknet_api_key"
    OPENWEATHER_API_KEY = "your_openweather_api_key"
    ```

4.  **Run the application:**
    ```bash
    streamlit run Home.py
    ```

## Deployment on Streamlit Cloud

1.  Push your code to a GitHub repository.
2.  Log in to [Streamlit Cloud](https://streamlit.io/cloud).
3.  Click "New app" and select your repository.
4.  Set the "Main file path" to `Home.py`.
5.  **Important**: Streamlit Cloud will automatically detect `packages.txt` and install Chromium.
6.  In the "Advanced settings", add your secrets (`OPENWEATHER_API_KEY`).
    - Note: `DATA_GOV_API_KEY` is no longer needed as we are scraping CommodityOnline.
7.  Click "Deploy".

### Selenium on Streamlit Cloud
This app uses Selenium to scrape price data.
- `packages.txt` ensures `chromium` and `chromium-driver` are installed.
- `utils/selenium_fetcher.py` is configured to use the system-installed Chromium binary in the cloud environment.

## Data Sources
- **AGMARKNET**: Agricultural Marketing Information Network for price data.
- **OpenWeatherMap**: For real-time weather updates.
