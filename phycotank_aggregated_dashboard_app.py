
import streamlit as st
import pandas as pd
import altair as alt

# Load the data
@st.cache_data
def load_data():
    return pd.read_csv("phycotank_array_dummy_data_filled.csv", parse_dates=["timestamp"])

df = load_data()

st.title("Phycotank Aggregated Dashboard")
st.markdown("### Summary of All Instrumented Phycotanks")

# Show data summary
st.markdown("#### Aggregated Metrics (Average per Hour)")
agg_df = df.groupby("timestamp").agg({
    "pH": "mean",
    "temperature_C": "mean",
    "flow_rate_lph": "mean",
    "energy_consumption_kWh": "mean",
    "lux": "mean",
    "mag_field_T": "mean"
}).reset_index()

metrics = ["pH", "temperature_C", "flow_rate_lph", "energy_consumption_kWh", "lux", "mag_field_T"]

# Time series charts
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

# Optional: Show raw aggregated data
if st.checkbox("Show Aggregated Data Table"):
    st.dataframe(agg_df)
