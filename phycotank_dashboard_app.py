
import streamlit as st
import pandas as pd
import altair as alt

# Load the data
@st.cache_data
def load_data():
    return pd.read_csv("phycotank_array_dummy_data_filled.csv", parse_dates=["timestamp"])

df = load_data()

st.title("Phycotank Dashboard")
st.markdown("### Algae Growth Monitoring from Instrumented Photobioreactors (PBRs)")

# Tank selector
tank_ids = df['phycotank_id'].unique()
selected_tank = st.selectbox("Select Phycotank", tank_ids)

# Filter by selected tank
filtered_df = df[df["phycotank_id"] == selected_tank]

# Time series charts
metrics = ["pH", "temperature_C", "flow_rate_lph", "energy_consumption_kWh", "lux", "mag_field_T"]

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

# Show raw data toggle
if st.checkbox("Show Raw Data"):
    st.dataframe(filtered_df)
