# sidebar.py
import streamlit as st
import os
from datetime import datetime

def show_sidebar():
    logo_path = "assets/nellie_carbon_capture_chip_logo_white.png"

    # Branding
    if os.path.exists(logo_path):
        st.sidebar.image(logo_path, use_container_width=True)
    else:
        st.sidebar.markdown("**Nellie Technologies Ltd**")

    st.sidebar.markdown("### Nellie CDR Platform")

    # Date/time
    st.sidebar.markdown(
        f"**{datetime.now().strftime('%A, %d %B %Y, %H:%M:%S')}**"
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown(f"© Nellie Technologies Ltd. {datetime.now().year}. All rights reserved.")