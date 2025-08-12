import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# Auto-refresh every 60 seconds
st_autorefresh(interval=60 * 1000, key="data_refresh")

# Load the data
@st.cache_data
def load_data():
    return pd.read_csv("phycotank_array_dummy_data_filled.csv", parse_dates=["timestamp"])

df = load_data()

# Sidebar branding
st.sidebar.image("nellie_carbon_capture_chip_logo_white.png", use_container_width=True)
st.sidebar.markdown("### Nellie Mwyndy Cross PhycoTank Array")

tank_options = ["Aggregate"] + sorted(df["phycotank_id"].unique())
selected_option = st.sidebar.selectbox("Select a phycotank", tank_options)

st.sidebar.markdown("Data ingested from Nellie Mwyndy Cross CDR Installation")
st.sidebar.markdown(f"**{datetime.now().strftime('%A, %d %B %Y, %H:%M:%S')}**")

st.sidebar.markdown("---")
st.sidebar.markdown(f"© Nellie Technologies Ltd. {datetime.now().year}. All rights reserved.")

# Main dashboard
st.title("Phycotank Monitoring Dashboard")

metrics = ["pH", "temperature_C", "flow_rate_lph", "energy_consumption_kWh", "lux", "mag_field_T"]

if selected_option == "Aggregate":
    st.header("Aggregated Metrics for All Instrumented Tanks")

    agg_df = df.groupby("timestamp").agg({metric: "mean" for metric in metrics}).reset_index()

    for metric in metrics:
        chart = alt.Chart(agg_df).mark_line().encode(
            x='timestamp:T',
            y=alt.Y(metric, title=metric.replace("_", " ").title()),
            tooltip=["timestamp:T", metric]
        ).properties(
            title=f"Average {metric.replace('_', ' ').title()} Over Time",
            width=700,
            height=300
        )
        st.altair_chart(chart, use_container_width=True)

    if st.sidebar.checkbox("Show Raw Data"):
        st.subheader("Aggregated Data Table")
        st.dataframe(agg_df)

else:
    st.header(f"Metrics for {selected_option}")

    filtered_df = df[df["phycotank_id"] == selected_option]

    for metric in metrics:
        chart = alt.Chart(filtered_df).mark_line().encode(
            x='timestamp:T',
            y=alt.Y(metric, title=metric.replace("_", " ").title()),
            tooltip=["timestamp:T", metric]
        ).properties(
            title=f"{metric.replace('_', ' ').title()} Over Time",
            width=700,
            height=300
        )
        st.altair_chart(chart, use_container_width=True)

    if st.sidebar.checkbox("Show Raw Data"):
        st.subheader(f"Raw Data for {selected_option}")
        st.dataframe(filtered_df)
