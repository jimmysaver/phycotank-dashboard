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
    # Tight top spacing via margin adjustments
    return (
        "<img src='data:image/png;base64,"
        + b64
        + "' style='width:100%;display:block;margin:0 0 .25rem 0;' alt='Nellie logo'/>"
    )

def show_sidebar():
    # --- Compact CSS, hide default Pages nav, pin footer, remove fullscreen on sidebar images ---
    st.markdown("""
        <style>
        /* Sidebar layout: flex so footer sticks to bottom */
        section[data-testid="stSidebar"] > div,
        section[data-testid="stSidebar"] div[data-testid="stSidebarContent"] {
            height: 100%;
            display: flex;
            flex-direction: column;
            padding-top: 0.5rem; /* reduce top padding */
        }
        /* Hide Streamlit's built-in multipage nav */
        div[data-testid="stSidebarNav"] { display: none !important; }

        /* Typography + spacing (compact) */
        .sidebar-title { font-weight: 600; font-size: 1rem; margin: .25rem 0 .25rem 0; }
        .sidebar-timestamp { font-size: .9rem; margin: 0 0 .5rem 0; }
        .sidebar-section { font-weight: 600; font-size: .9rem; margin: .5rem 0 .25rem 0; }
        .sidebar-menu a { display:block; padding: .2rem 0; text-decoration:none; }
        .sidebar-sep { margin: .5rem 0; border: 0; border-top: 1px solid #e6e6e6; }

        /* Footer styling + placement */
        .sidebar-footer { margin-top: auto; font-size: 0.85rem; opacity: 0.8; }

        /* Hide fullscreen hover button for any images in the sidebar */
        section[data-testid="stSidebar"] button[title="View fullscreen"] {
            display: none !important;
        }
        </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        # --- Logo (base64 embed = no fullscreen control) ---
        logo_path = "assets/nellie_carbon_capture_chip_logo_white.png"
        if os.path.exists(logo_path):
            st.markdown(_embed_logo_base64(logo_path), unsafe_allow_html=True)
        else:
            st.markdown("**Nellie Technologies Ltd**")

        # --- Title + timestamp (compact) ---
        st.markdown("<div class='sidebar-title'>Nellie CDR System</div>", unsafe_allow_html=True)
        uk_now = datetime.now(ZoneInfo("Europe/London")).strftime("%A, %d %B %Y, %H:%M:%S")
        st.markdown(f"<div class='sidebar-timestamp'><strong>{uk_now}</strong></div>", unsafe_allow_html=True)

        st.markdown("<hr class='sidebar-sep'/>", unsafe_allow_html=True)
        st.markdown("<div class='sidebar-section'>Menu</div>", unsafe_allow_html=True)

        # --- Custom menu (no emojis/icons) ---
        try:
            st.page_link("Nellie.py", label="Home")
            st.page_link("pages/1_Phycotank_Array.py", label="Phycotank Array")
            # Add more pages when ready, e.g.:
            # st.page_link("pages/2_Biomass_Dehydration.py", label="Biomass Dehydration")
            # st.page_link("pages/3_Pyrolysis.py", label="Pyrolysis Operations")
            # st.page_link("pages/4_Permanence.py", label="Permanence & Sequestration")
        except Exception:
            # Fallback if page_link isn't available
            st.markdown(
                "<div class='sidebar-menu'>"
                "<a href='./'>Home</a>"
                "<a href='./Phycotank_Array'>Phycotank Array</a>"
                "</div>",
                unsafe_allow_html=True
            )

        # --- Footer pinned at bottom ---
        year = datetime.now(ZoneInfo("Europe/London")).year
        st.markdown(
            f"<div class='sidebar-footer'>© Nellie Technologies Ltd. {year}. All rights reserved.</div>",
            unsafe_allow_html=True
        )