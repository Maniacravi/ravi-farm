import streamlit as st

st.set_page_config(
    page_title="Farm Insights",
    page_icon="🌱",
    layout="wide",
)

st.title("Farm Insights")
st.subheader("A clean starting point for your data-driven Streamlit site.")

st.markdown(
    """
Welcome to your reset project. This starter layout keeps your **assets** and **data**
folders intact while giving you a lightweight, maintainable Streamlit foundation.

Use this Home page as your landing space to highlight key metrics, showcase visuals,
or provide links to the most important parts of your project.
    """
)

st.divider()

st.markdown("### Quick highlights")

col1, col2, col3 = st.columns(3)
col1.metric("Pages", "2", "Home & Info")
col2.metric("Assets folder", "Ready", help="Drop images or branding here.")
col3.metric("Data folder", "Ready", help="Add CSVs or other data sources.")

st.markdown("### Getting started")

st.markdown(
    """
- Add your datasets to `data/` and access them with `pandas`, `pyarrow`, or your
  preferred library.
- Place logos, icons, or other static files in `assets/` and reference them by
  relative path.
- Duplicate this page or create new modules in the `pages/` directory to expand
  the app.
- Use Streamlit components like columns, tabs, charts, and forms to build out your UI.
    """
)

st.info(
    "Tip: Rename page files to control display order (e.g., `1_Home.py`, `2_Info.py`)."
)

st.success(
    "You're all set! Customize this page with charts, summaries, or calls-to-action."
)
