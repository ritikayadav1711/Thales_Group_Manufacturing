import streamlit as st
import pandas as pd

st.title("Thales Smart Factory Dashboard")

df = pd.read_csv("Thales_Group_Manufacturing.csv")

st.dataframe(df.head())
st.subheader("Factory Health Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Machines", df["Machine_ID"].nunique())
col2.metric("Avg Temperature", round(df["Temperature_C"].mean(), 2))
col3.metric("Avg Vibration", round(df["Vibration_Hz"].mean(), 2))
col4.metric("Avg Production Speed", round(df["Production_Speed_units_per_hr"].mean(), 2))
st.subheader("Efficiency Status Distribution")

efficiency_count = df["Efficiency_Status"].value_counts()
st.bar_chart(efficiency_count)
st.subheader("Operation Mode Distribution")

mode_count = df["Operation_Mode"].value_counts()
st.bar_chart(mode_count)
st.subheader("Operation Mode Distribution")
st.sidebar.header("Filters")

selected_machine = st.sidebar.selectbox(
    "Select Machine",
    sorted(df["Machine_ID"].unique())
)

machine_df = df[df["Machine_ID"] == selected_machine]

st.subheader(f"Machine {selected_machine} Health Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Avg Temperature", round(machine_df["Temperature_C"].mean(), 2))
col2.metric("Avg Vibration", round(machine_df["Vibration_Hz"].mean(), 2))
col3.metric("Avg Power", round(machine_df["Power_Consumption_kW"].mean(), 2))
st.subheader("Top Risk Machines")

machine_health = df.groupby("Machine_ID").agg({
    "Temperature_C": "mean",
    "Vibration_Hz": "mean",
    "Power_Consumption_kW": "mean",
    "Quality_Control_Defect_Rate_%": "mean",
    "Error_Rate_%": "mean"
}).reset_index()

machine_health["Risk_Score"] = (
    machine_health["Temperature_C"] * 0.25 +
    machine_health["Vibration_Hz"] * 10 * 0.25 +
    machine_health["Power_Consumption_kW"] * 5 * 0.20 +
    machine_health["Quality_Control_Defect_Rate_%"] * 0.20 +
    machine_health["Error_Rate_%"] * 0.10
)

top_risk = machine_health.sort_values("Risk_Score", ascending=False).head(10)

st.dataframe(top_risk)

st.bar_chart(top_risk.set_index("Machine_ID")["Risk_Score"])
st.subheader("Production Speed vs Defect Rate")

chart_data = df[[
    "Production_Speed_units_per_hr",
    "Quality_Control_Defect_Rate_%"
]]

st.scatter_chart(
    chart_data,
    x="Production_Speed_units_per_hr",
    y="Quality_Control_Defect_Rate_%"
)
st.subheader("Temperature vs Defect Rate")

st.scatter_chart(
    df,
    x="Temperature_C",
    y="Quality_Control_Defect_Rate_%"
)
st.subheader("Vibration vs Error Rate")

st.scatter_chart(
    df,
    x="Vibration_Hz",
    y="Error_Rate_%"
)
st.subheader("Business Recommendations")

st.markdown("""
1. Monitor machines with high temperature and vibration.
2. Prioritize top-risk machines for preventive maintenance.
3. Investigate machines with high defect and error rates.
4. Improve production planning for low-efficiency operations.
5. Use the dashboard regularly for operational decision-making.
""")
