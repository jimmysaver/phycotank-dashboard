# utils/sidebar.py
import os
import base64
from datetime import datetime
from zoneinfo import ZoneInfo
import streamlit as st

def _embed_logo_base64(path: str) -> str:
    """Return an <img> tag with the file embedded as base64; no fullscreen button."""
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    return f"<img src='data:image/png;base64,{b64}' style='width:100%;display:block;' alt='Nellie logo'/>"

def show_sidebar():
    # ---- CSS: layout + hide Streamlit’s built-in sidebar pages nav, pin footer at bottom ----
    st.markdown("""
        <style>
        /* Sidebar as flex column so we can push footer down */
        section[data-testid="stSidebar"] > div,
        section[data-testid="stSidebar"] div[data-testid="stSidebarContent"] {
            height: 100%;
            display: flex;
            flex-direction: column;
        }
        /* Hide the default multipage navigation so only our custom menu shows */
        div[data-testid="stSidebarNav"] { display: none !important; }
        /* Footer styling + placement */
        .sidebar-footer { margin-top: auto; font-size: 0.85rem; opacity: 0.8; }
        </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        # --- Logo (base64-embedded, no fullscreen hover) ---
        logo_path = "assets/nellie_carbon_capture_chip_logo_white.png"
        if os.path.exists(logo_path):
            st.markdown(_embed_logo_base64(logo_path), unsafe_allow_html=True)
        else:
            st.markdown("**Nellie Technologies Ltd**")

        # --- Title + time ---
        st.markdown("### Nellie CDR System")
        uk_now = datetime.now(ZoneInfo("Europe/London")).strftime("%A, %d %B %Y, %H:%M:%S")
        st.markdown(f"**{uk_now}**")

        st.markdown("---")
        st.markdown("#### Menu")

        # --- Custom menu (use page_link if available; otherwise fallback) ---
        try:
            st.page_link("Nellie.py", label="Home", icon="🏠")
            st.page_link("pages/1_Phycotank_Array.py", label="Phycotank Array", icon="📈")
            # Add more when ready:
            # st.page_link("pages/2_Biomass_Dehydration.py", label="Biomass Dehydration", icon="💧")
            # st.page_link("pages/3_Pyrolysis.py", label="Pyrolysis Operations", icon="🔥")
            # st.page_link("pages/4_Permanence.py", label="Permanence & Sequestration", icon="🌍")
        except Exception:
            st.markdown("""
            - [Home](./)
            - [Phycotank Array](./Phycotank_Array)
            """)

        # --- Footer pinned at bottom ---
        year = datetime.now(ZoneInfo("Europe/London")).year
        st.markdown(
            f"<div class='sidebar-footer'>© Nellie Technologies Ltd. {year}. All rights reserved.</div>",
            unsafe_allow_html=True
        )