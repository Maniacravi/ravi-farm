import streamlit as st

st.set_page_config(page_title="Info", page_icon="ℹ️", layout="wide")

st.title("Project Information")
st.markdown(
    """
Use this page to document what the app does, how data is organized, and how to extend
it. Update the sections below with details specific to your project.
    """
)

st.header("Structure at a glance")
st.markdown(
    """
- `assets/`: Store static files such as images, icons, and CSS. Reference them by
  relative path (e.g., `assets/logo.png`).
- `data/`: Keep raw and processed datasets here. Load them using `pandas`, `pyarrow`,
  or your preferred data library.
- `Home.py`: Landing page for the application. Add KPIs, charts, or navigation links.
- `pages/`: Place additional Streamlit pages in this folder to expand the app.
    """
)

st.header("How to extend")
st.markdown(
    """
1. Duplicate an existing page file (e.g., `pages/Info.py`) and adjust the content.
2. Add shared helpers or loaders in a new module (e.g., `lib/` or `services/`) as the
   project grows.
3. Use `st.cache_data` or `st.cache_resource` to memoize expensive operations.
4. Keep secrets and credentials out of source control; rely on environment variables
   or Streamlit's secrets management.
    """
)

st.header("Next steps")
st.markdown(
    """
- Add branding assets and reference them in your UI components.
- Wire up data loading and simple visualizations to validate datasets.
- Integrate authentication or role-based views if you expect different user types.
- Set up CI to lint and test your Streamlit app before deployment.
    """
)

st.success("Document important decisions here so new collaborators can ramp up quickly.")
