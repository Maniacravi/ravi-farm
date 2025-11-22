import streamlit as st
from pathlib import Path

IMAGE_DIR = Path("assets/farm_photos")
VALID_SUFFIXES = {".jpg", ".jpeg", ".png", ".gif"}
IMAGE_PATHS = sorted(
    [p for p in IMAGE_DIR.glob("*") if p.suffix.lower() in VALID_SUFFIXES],
    key=lambda p: p.name.lower(),
)
IMAGE_CAPTIONS = [p.stem.replace("_", " ").title() for p in IMAGE_PATHS]

st.title("🏡 About Ravi Farm")
if IMAGE_PATHS:
    st.subheader("📸 Farm Photo Gallery")
    st.markdown(
        """
        <style>
        .gallery-block {
            max-width: 1000px;
            margin: 0 auto 1.5rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    for path, caption in zip(IMAGE_PATHS, IMAGE_CAPTIONS):
        st.markdown('<div class="gallery-block">', unsafe_allow_html=True)
        st.image(str(path), width="stretch")
        st.caption(caption)
        st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info("Add farm photos (jpg/jpeg/png/gif) under `assets/farm_photos/` to see them here.")

st.markdown("""
Welcome to **Ravi Farm**, a family-run lime and fruit orchard located in **Rajapalayam, Tamil Nadu**.

We believe in sustainable farming — combining traditional practices with modern analytics
to improve crop yield, water efficiency, and soil health.

**What we grow:**  
- Limes 🍋  
- Bananas 🍌  
- Seasonal vegetables 🌱  

**Our mission:** Better data, better harvest, better planet 🌍.
""")
