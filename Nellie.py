# Nellie.py - Millie Platform Command Centre

import streamlit as st
from datetime import datetime
import pytz
from streamlit_autorefresh import st_autorefresh

# Auto-refresh every 60 seconds
st_autorefresh(interval=60 * 1000, key="main_refresh")

# --- TIMEZONE ---
tz = pytz.timezone("Europe/London")
current_time = datetime.now(tz).strftime('%A, %d %B %Y, %H:%M:%S')

import os

# Nellie.py
import streamlit as st
from sidebar import show_sidebar

st.set_page_config(page_title="Nellie CDR Dashboard", layout="wide")

# Show the sidebar
show_sidebar()

st.title("Nellie Carbon Dioxide Removal System")

st.markdown("""
Welcome to the Nellie CDR Platform — view live metrics and insights
for the full carbon removal lifecycle:
- **Phycotanks**
- **Biomass Dehydration**
- **Pyrolysis & Biochar**
- **Sequestration Sites**
""")

# Navigation (Streamlit's multipage feature)
st.markdown("Use the sidebar to navigate between dashboards.")

# Try assets folder first, then root directory
logo_paths = [
    "assets/nellie_carbon_capture_chip_logo_white.png",
    "nellie_carbon_capture_chip_logo_white.png"
]

logo_path = next((path for path in logo_paths if os.path.exists(path)), None)

if logo_path:
    st.sidebar.image(logo_path, use_container_width=True)
else:
    st.sidebar.warning("Logo not found")

# --- SIDEBAR ---
st.sidebar.image("assets/nellie_carbon_capture_chip_logo_white.png", use_container_width=True)
st.sidebar.markdown("### Millie Platform — CDR Command Centre")
st.sidebar.markdown("Data across **Phycotanks, Biomass Processing, Pyrolysis,** and **Sequestration Sites**")
st.sidebar.markdown(f"**{current_time}**")
st.sidebar.markdown("---")
st.sidebar.markdown(f"© Nellie Technologies Ltd. {datetime.now().year}. All rights reserved.")

# --- MAIN DASHBOARD TITLE ---
st.title("🌍 Millie Platform — Carbon Dioxide Removal System Overview")

st.markdown("""
Welcome to the **Millie Platform Command Centre** — a real-time dashboard for monitoring every stage of our carbon removal process:
1. **Phycotanks** — Growth performance, environmental metrics, and CO₂ capture rates.
2. **Biomass Dehydration** — Processing throughput and energy use.
3. **Pyrolysis** — Biochar output, reactor efficiency, and energy balance.
4. **Permanence & Sequestration Sites** — Tracking CO₂ stored and validating permanence.
""")

# --- MOCK SUMMARY METRICS (Replace with live DB/API later) ---
col1, col2, col3 = st.columns(3)
col1.metric("Total CO₂ Captured", "126,540 kg", "+540 kg")
col2.metric("Biochar Produced", "42,180 kg", "+210 kg")
col3.metric("Active Sequestration Sites", "8", "+1")

col4, col5, col6 = st.columns(3)
col4.metric("Avg Phycotank pH", "7.6", "Stable")
col5.metric("Dehydration Energy Use", "1.3 MWh", "-2%")
col6.metric("Pyrolysis Energy Use", "2.1 MWh", "+1%")

st.markdown("---")

# --- PAGE LINKS ---
st.subheader("📊 Explore Detailed Dashboards")
st.markdown("""
- [Phycotank Array Dashboard](./Phycotank_Array)
- [Biomass Dehydration](./Biomass_Dehydration)
- [Pyrolysis Operations](./Pyrolysis)
- [Permanence & Sequestration Sites](./Permanence)
""")

st.info("These sections load detailed visualisations and historical trends for each stage of the process.")