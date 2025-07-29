
import streamlit as st
import pandas as pd
import altair as alt

# Load the data
@st.cache_data
def load_data():
    return pd.read_csv("phycotank_array_dummy_data_filled.csv", parse_dates=["timestamp"])

df = load_data()

# Sidebar for tank selection
st.sidebar.title("Phycotank Selector")
tank_options = ["Aggregate"] + sorted(df["phycotank_id"].unique())
selected_option = st.sidebar.selectbox("Select a phycotank", tank_options)

st.title("Phycotank Monitoring Dashboard")

if selected_option == "Aggregate":
    st.header("Aggregated Metrics for All Instrumented Tanks")

    agg_df = df.groupby("timestamp").agg({
        "pH": "mean",
        "temperature_C": "mean",
        "flow_rate_lph": "mean",
        "energy_consumption_kWh": "mean",
        "lux": "mean",
        "mag_field_T": "mean"
    }).reset_index()

    metrics = ["pH", "temperature_C", "flow_rate_lph", "energy_consumption_kWh", "lux", "mag_field_T"]
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

else:
    st.header(f"Metrics for {selected_option}")

    filtered_df = df[df["phycotank_id"] == selected_option]
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

if st.sidebar.checkbox("Show Raw Data"):
    if selected_option == "Aggregate":
        st.subheader("Aggregated Data Table")
        st.dataframe(agg_df)
    else:
        st.subheader(f"Raw Data for {selected_option}")
        st.dataframe(filtered_df)
