import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.set_page_config(page_title="Rocket Mission Dashboard", layout="wide")

st.title("🚀 Space Rocket Mission Dashboard")

# ===============================
# LOAD DATA
# ===============================

df = pd.read_csv("cleaned_missions.csv")

# ===============================
# CLEAN DATA (Safety)
# ===============================

df.columns = df.columns.str.strip()

df["Launch Date"] = pd.to_datetime(df["Launch Date"], errors="coerce")

numeric_columns = [
    "Distance from Earth (light-years)",
    "Mission Duration (years)",
    "Mission Cost (billion USD)",
    "Scientific Yield (points)",
    "Crew Size",
    "Mission Success (%)",
    "Fuel Consumption (tons)",
    "Payload Weight (tons)"
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna()

# ===============================
# OPTIONAL FILTERS
# ===============================

st.sidebar.header("Filters")

mission_type = st.sidebar.selectbox(
    "Select Mission Type",
    ["All"] + list(df["Mission Type"].unique())
)

launch_vehicle = st.sidebar.selectbox(
    "Select Launch Vehicle",
    ["All"] + list(df["Launch Vehicle"].unique())
)

cost_range = st.sidebar.slider(
    "Select Mission Cost Range (billion USD)",
    float(df["Mission Cost (billion USD)"].min()),
    float(df["Mission Cost (billion USD)"].max()),
    (float(df["Mission Cost (billion USD)"].min()),
     float(df["Mission Cost (billion USD)"].max()))
)

# Apply filters
filtered_df = df.copy()

if mission_type != "All":
    filtered_df = filtered_df[filtered_df["Mission Type"] == mission_type]

if launch_vehicle != "All":
    filtered_df = filtered_df[filtered_df["Launch Vehicle"] == launch_vehicle]

filtered_df = filtered_df[
    (filtered_df["Mission Cost (billion USD)"] >= cost_range[0]) &
    (filtered_df["Mission Cost (billion USD)"] <= cost_range[1])
]

# ===============================
# VISUALIZATIONS
# ===============================

st.header("📊 Mission Data Analysis")

col1, col2 = st.columns(2)

# 1️⃣ Scatter: Payload vs Fuel
with col1:
    st.subheader("Payload Weight vs Fuel Consumption")
    fig1 = px.scatter(
        filtered_df,
        x="Payload Weight (tons)",
        y="Fuel Consumption (tons)",
        hover_name="Mission Name"
    )
    st.plotly_chart(fig1, use_container_width=True)

# 2️⃣ Bar: Cost vs Success
with col2:
    st.subheader("Mission Cost: Success vs Failure")
    filtered_df["Success Category"] = np.where(
        filtered_df["Mission Success (%)"] >= 50,
        "Successful",
        "Failed"
    )
    cost_by_success = filtered_df.groupby("Success Category")[
        "Mission Cost (billion USD)"
    ].mean().reset_index()

    fig2 = px.bar(
        cost_by_success,
        x="Success Category",
        y="Mission Cost (billion USD)"
    )
    st.plotly_chart(fig2, use_container_width=True)

# 3️⃣ Line: Duration vs Distance
st.subheader("Mission Duration vs Distance from Earth")
fig3 = px.line(
    filtered_df,
    x="Mission Duration (years)",
    y="Distance from Earth (light-years)"
)
st.plotly_chart(fig3, use_container_width=True)

# 4️⃣ Box Plot: Crew vs Success
st.subheader("Crew Size vs Mission Success (%)")
fig4 = px.box(
    filtered_df,
    x="Crew Size",
    y="Mission Success (%)"
)
st.plotly_chart(fig4, use_container_width=True)

# 5️⃣ Scatter: Scientific Yield vs Cost
st.subheader("Scientific Yield vs Mission Cost")
fig5 = px.scatter(
    filtered_df,
    x="Mission Cost (billion USD)",
    y="Scientific Yield (points)"
)
st.plotly_chart(fig5, use_container_width=True)

# ===============================
# HEATMAP
# ===============================

st.subheader("Correlation Heatmap")

numeric_df = filtered_df[numeric_columns]

fig6, ax = plt.subplots()
sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", ax=ax)
st.pyplot(fig6)

# ===============================
# SIMPLE ROCKET SIMULATION
# ===============================

st.header("🚀 Rocket Launch Simulation")

mass = st.slider("Initial Mass (kg)", 100000, 800000, 500000)
thrust = st.slider("Thrust (Newtons)", 1000000, 10000000, 7000000)

g = 9.81
dt = 0.1
time_steps = 200

velocity = 0
altitude = 0

altitudes = []

for t in range(time_steps):
    gravity_force = mass * g
    net_force = thrust - gravity_force
    acceleration = net_force / mass
    
    velocity += acceleration * dt
    altitude += velocity * dt
    
    altitudes.append(altitude)

sim_df = pd.DataFrame({
    "Time": range(time_steps),
    "Altitude": altitudes
})

fig7 = px.line(sim_df, x="Time", y="Altitude")
st.plotly_chart(fig7, use_container_width=True)

st.success("Dashboard Loaded Successfully 🚀")
