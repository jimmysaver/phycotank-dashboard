# Nellie.py — Millie Platform Command Centre (clean, sidebar-driven nav)

import streamlit as st
from streamlit_autorefresh import st_autorefresh

# Page config must be first
st.set_page_config(page_title="Nellie CDR Dashboard", layout="wide")

# Shared sidebar (logo, timestamp, menu, footer)
from utils.sidebar import show_sidebar
show_sidebar()

# Auto-refresh every 60 seconds (keeps timestamp + data fresh)
st_autorefresh(interval=60 * 1000, key="main_refresh")

# ------------------ MAIN ------------------
st.title("Nellie Carbon Dioxide Removal System")

st.markdown("""
Welcome to the Nellie CDR Platform — view live metrics and insights
for the full carbon removal lifecycle:
- **Phycotanks**
- **Biomass Dehydration**
- **Pyrolysis & Biochar**
- **Sequestration Sites**
""")

st.markdown("## 🌍 System Overview")

# Summary metrics (mock placeholders for now)
c1, c2, c3 = st.columns(3)
c1.metric("Total CO₂ Captured", "126,540 kg", "+540 kg")
c2.metric("Biochar Produced", "42,180 kg", "+210 kg")
c3.metric("Active Sequestration Sites", "8", "+1")

c4, c5, c6 = st.columns(3)
c4.metric("Avg Phycotank pH", "7.6", "Stable")
c5.metric("Dehydration Energy Use", "1.3 MWh", "-2%")
c6.metric("Pyrolysis Energy Use", "2.1 MWh", "+1%")

st.info("Use the **sidebar menu** to open detailed dashboards.")