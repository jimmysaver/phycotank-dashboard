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
    # Compact top/bottom spacing
    return (
        "<img src='data:image/png;base64,"
        + b64
        + "' style='width:100%;display:block;margin:0 0 .25rem 0;' alt='Nellie logo'/>"
    )

def show_sidebar():
    # --- CSS: compact layout, hide default nav, pin footer, remove fullscreen on sidebar images ---
    st.markdown("""
        <style>
        /* Sidebar as flex column so footer stays at bottom; reduce top padding */
        section[data-testid="stSidebar"] > div,
        section[data-testid="stSidebar"] div[data-testid="stSidebarContent"] {
            height: 100%;
            display: flex;
            flex-direction: column;
            padding-top: 0.5rem;
        }
        /* Hide Streamlit's built-in multipage nav (we use our own menu) */
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
        section[data-testid="stSidebar"] button[title="View fullscreen"] { display: none !important; }
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

        # --- Custom menu (lowercase files) ---
        try:
            # Top-level / operations
            st.page_link("Nellie.py", label="Home")
            st.page_link("pages/01_system_overview.py", label="System Overview")
            st.page_link("pages/02_array_operations.py", label="Array Operations")
            st.page_link("pages/03_dehydration_operations.py", label="Dehydration Operations")
            st.page_link("pages/04_pyrolysis_operations.py", label="Pyrolysis Operations")

            st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
            st.page_link("pages/05_production.py", label="Production")
            st.page_link("pages/06_batch_detail_list.py", label="Batch Detail (List)")
            st.page_link("pages/07_Lab_Results_List.py", label="Lab Results (List)")
# no link to detail page here

            st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
            st.page_link("pages/08_site_data.py", label="Site Data")
            st.page_link("pages/09_insurances.py", label="Insurances")
            st.page_link("pages/10_permits.py", label="Permits")
            st.page_link("pages/11_tea.py", label="TEA")
            st.page_link("pages/12_lca.py", label="LCA (placeholder)")
        except Exception:
            # Fallback simple HTML links if st.page_link isn't available
            st.markdown(
                "<div class='sidebar-menu'>"
                "<a href='./'>Home</a>"
                "<a href='./system_overview'>System Overview</a>"
                "<a href='./array_operations'>Array Operations</a>"
                "<a href='./dehydration_operations'>Dehydration Operations</a>"
                "<a href='./pyrolysis_operations'>Pyrolysis Operations</a>"
                "<br/>"
                "<a href='./production'>Production</a>"
                "<a href='./batch_detail_list'>Batch Detail (List)</a>"
                "<a href='./lab_results_list'>Lab Results (List)</a>"
                "<br/>"
                "<a href='./site_data'>Site Data</a>"
                "<a href='./insurances'>Insurances</a>"
                "<a href='./permits'>Permits</a>"
                "<a href='./tea'>TEA</a>"
                "<a href='./lca'>LCA (placeholder)</a>"
                "</div>",
                unsafe_allow_html=True
            )

        # --- Footer pinned at bottom ---
        year = datetime.now(ZoneInfo("Europe/London")).year
        st.markdown(
            f"<div class='sidebar-footer'>© Nellie Technologies Ltd. {year}. All rights reserved.</div>",
            unsafe_allow_html=True
        )