# pages/1_Phycotank_Array.py
import streamlit as st
import pandas as pd
import altair as alt

st.title("Phycotank Array — Monitoring")

# --- Data loader ---
@st.cache_data
def load_data():
    # CSV must be in the repo root (adjust path if you moved it)
    return pd.read_csv("phycotank_array_dummy_data_filled.csv", parse_dates=["timestamp"])

df = load_data()

# --- Controls (sidebar) ---
st.sidebar.subheader("Phycotank Controls")
tank_options = ["Aggregate"] + sorted(df["phycotank_id"].unique())
selected_option = st.sidebar.selectbox("Select a phycotank", tank_options)
show_raw = st.sidebar.checkbox("Show raw data")

# --- Metrics to plot ---
metrics = [
    "pH",
    "temperature_C",
    "flow_rate_lph",
    "energy_consumption_kWh",
    "lux",
    "mag_field_T",
]

# --- Charts ---
if selected_option == "Aggregate":
    st.header("Aggregated Metrics (All Instrumented Tanks)")
    agg_df = df.groupby("timestamp", as_index=False)[metrics].mean()

    for metric in metrics:
        chart = (
            alt.Chart(agg_df)
            .mark_line()
            .encode(
                x="timestamp:T",
                y=alt.Y(metric, title=metric.replace("_", " ").title()),
                tooltip=["timestamp:T", metric],
            )
            .properties(
                title=f"Average {metric.replace('_', ' ').title()} Over Time",
                height=300,
            )
        )
        st.altair_chart(chart, use_container_width=True)

    if show_raw:
        st.subheader("Aggregated Data Table")
        st.dataframe(agg_df, use_container_width=True)

else:
    st.header(f"Metrics for {selected_option}")
    filtered = df[df["phycotank_id"] == selected_option].copy()

    for metric in metrics:
        chart = (
            alt.Chart(filtered)
            .mark_line()
            .encode(
                x="timestamp:T",
                y=alt.Y(metric, title=metric.replace("_", " ").title()),
                tooltip=["timestamp:T", metric],
            )
            .properties(
                title=f"{metric.replace('_', ' ').title()} Over Time — {selected_option}",
                height=300,
            )
        )
        st.altair_chart(chart, use_container_width=True)

    if show_raw:
        st.subheader(f"Raw Data — {selected_option}")
        st.dataframe(filtered, use_container_width=True)