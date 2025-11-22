# Farm Insights Streamlit Starter

This repository is a clean starting point for a two-page Streamlit application. All
previous code has been removed, keeping only your existing `assets/` and `data/`
directories.

## Project layout
- `Home.py` — landing page for the application.
- `pages/Info.py` — info/documentation page.
- `assets/` — static files such as images, icons, and stylesheets.
- `data/` — datasets you want to load and explore.

## Getting started
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the app:
   ```bash
   streamlit run Home.py
   ```
3. Add more pages by creating new Python files in the `pages/` directory.

## Customization tips
- Reference static assets with relative paths, e.g. `assets/logo.png`.
- Use `st.cache_data` to memoize data loading and keep the UI snappy.
- Add tests or linting as the project grows to maintain quality.
