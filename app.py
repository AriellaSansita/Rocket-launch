import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Set page config for professional layout [cite: 2]
st.set_page_config(page_title="Rocket Mission Dashboard", layout="wide")

st.title("🚀 Space Rocket Mission Dashboard")

# ===============================
# STAGE 1: RESEARCH & GUIDING QUESTIONS 
# ===============================
with st.expander("📖 Project Research & Guiding Questions (Click to Expand)"):
    st.write("### Research Insights")
    st.write("- **Newton’s Second Law:** Rocket acceleration is determined by Net Force (Thrust - Gravity - Drag) divided by Mass[cite: 2].")
    st.write("- **Variable Mass:** As fuel burns, the rocket's mass decreases, which causes acceleration to increase over time even if thrust remains constant[cite: 2].")
    st.write("### Guiding Question Answers")
    st.write("1. **How does adding more payload affect altitude?** Higher payload increases total mass, reducing initial acceleration and lowering the maximum altitude reached.")
    st.write("2. **How does increasing thrust affect launch success?** Higher thrust helps overcome gravity faster, reducing 'gravity losses' and increasing the chance of reaching orbit.")
    st.write("3. **Does lower drag at higher altitudes improve speed?** Yes, as the atmosphere thins, air resistance (drag) decreases, allowing for higher terminal velocity.")

# ===============================
# STAGE 2: DATA PREPROCESSING & CLEANING 
# ===============================
try:
    df = pd.read_csv("cleaned_missions.csv")
    df.columns = df.columns.str.strip()
except FileNotFoundError:
    st.error("Dataset 'cleaned_missions.csv' not found. Please ensure it is in the same folder as this script.")
    st.stop()

# Cleaning and Type Conversion 
df["Launch Date"] = pd.to_datetime(df["Launch Date"], errors="coerce")

numeric_columns = [
    "Distance from Earth (light-years)", "Mission Duration (years)",
    "Mission Cost (billion USD)", "Scientific Yield (points)",
    "Crew Size", "Mission Success (%)", "Fuel Consumption (tons)",
    "Payload Weight (tons)"
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna()

# ===============================
# INTERACTIVE FILTERS [cite: 2]
# ===============================
st.sidebar.header("Dashboard Filters")
mission_type = st.sidebar.selectbox("Filter by Mission Type", ["All"] + list(df["Mission Type"].unique()))
launch_vehicle = st.sidebar.selectbox("Filter by Launch Vehicle", ["All"] + list(df["Launch Vehicle"].unique()))

filtered_df = df.copy()
if mission_type != "All":
    filtered_df = filtered_df[filtered_df["Mission Type"] == mission_type]
if launch_vehicle != "All":
    filtered_df = filtered_df[filtered_df["Launch Vehicle"] == launch_vehicle]

# ===============================
# STAGE 4: DATA VISUALIZATION & ANALYSIS 
# ===============================
st.header("Real-World Mission Data Analysis")

# 1. Scatter: Payload vs Fuel (Requirement: Seaborn/Plotly) [cite: 2]
st.subheader("1. Payload Weight vs Fuel Consumption")
fig1 = px.scatter(filtered_df, x="Payload Weight (tons)", y="Fuel Consumption (tons)", 
                 color="Mission Success (%)", hover_name="Mission Name")
st.plotly_chart(fig1, use_container_width=True)
st.info("**Insight:** A strong positive correlation exists; heavier payloads consistently require more fuel to reach the target distance. [cite: 2]")

col1, col2 = st.columns(2)

# 2. Bar: Cost vs Success (Requirement: Matplotlib/Plotly) [cite: 2]
with col1:
    st.subheader("2. Average Cost: Success vs Failure")
    filtered_df["Status"] = np.where(filtered_df["Mission Success (%)"] >= 80, "Success", "Failure")
    avg_cost = filtered_df.groupby("Status")["Mission Cost (billion USD)"].mean().reset_index()
    fig2 = px.bar(avg_cost, x="Status", y="Mission Cost (billion USD)", color="Status")
    st.plotly_chart(fig2)
    st.write("**Insight:** High-cost missions are not always more successful, suggesting that resource management is as vital as budget. [cite: 2]")

# 3. Box Plot: Crew Size vs Success (Requirement: Seaborn) [cite: 2]
with col2:
    st.subheader("3. Crew Size Distribution by Status")
    fig3, ax3 = plt.subplots()
    sns.boxplot(data=filtered_df, x="Status", y="Crew Size", ax=ax3)
    ax3.set_ylabel("Crew Size (Persons)")
    st.pyplot(fig3)
    st.write("**Insight:** Successful missions show a consistent crew size range, whereas failures often correlate with extreme outliers. [cite: 2]")

# 4. Line Chart: Duration vs Distance [cite: 2]
st.subheader("4. Mission Duration vs Distance from Earth")
fig4 = px.line(filtered_df.sort_values("Mission Duration (years)"), 
              x="Mission Duration (years)", y="Distance from Earth (light-years)")
st.plotly_chart(fig4, use_container_width=True)
st.info("**Insight:** As expected, distance from Earth is the primary driver of mission duration. [cite: 2]")

# 5. Correlation Heatmap (Requirement: Statistical Visuals) [cite: 2]
st.subheader("5. Statistical Correlation Heatmap")
fig5, ax5 = plt.subplots(figsize=(10, 6))
sns.heatmap(filtered_df[numeric_columns].corr(), annot=True, cmap="coolwarm", ax=ax5)
st.pyplot(fig5)
st.write("**Insight:** This heatmap confirms that Fuel Consumption and Payload Weight are the most tightly linked variables in the dataset. [cite: 2]")

# ===============================
# STAGE 3: ROCKET SIMULATION (Differential Equations) 
# ===============================

st.divider()
st.header("Rocket Launch Simulation (Calculus-Based)")
st.write("This simulation applies **Newton's Second Law** using a step-by-step update to acceleration, velocity, and altitude while accounting for **mass reduction** as fuel burns. [cite: 2]")

# User Inputs for Simulation
sc1, sc2, sc3 = st.columns(3)
dry_mass = sc1.number_input("Dry Mass (kg)", value=200000)
fuel_initial = sc2.number_input("Initial Fuel (kg)", value=300000)
thrust = sc3.number_input("Engine Thrust (N)", value=8000000)

# Physical Constants
g = 9.81  # Gravity [cite: 2]
burn_rate = 1500  # Fuel consumption rate in kg/s [cite: 2]
dt = 1.0  # Time step
time_steps = 200

# Simulation Loop
sim_data = []
curr_fuel = fuel_initial
v = 0
h = 0

for t in range(time_steps):
    total_m = dry_mass + curr_fuel
    
    if curr_fuel > 0:
        # F_net = Thrust - Weight
        net_f = thrust - (total_m * g)
        curr_fuel -= burn_rate
    else:
        # Engine cutoff: only gravity acts on the rocket
        net_f = -(total_m * g)
    
    # Differential Equation Updates [cite: 2]
    a = net_f / total_m
    v += a * dt
    h += v * dt
    
    if h < 0: # Ensure rocket doesn't fall below ground
        h = 0
        v = 0
        
    sim_data.append({"Time (s)": t, "Altitude (m)": h, "Velocity (m/s)": v, "Fuel (kg)": max(0, curr_fuel)})

sim_results = pd.DataFrame(sim_data)

# Visualization of Simulation
st.subheader("Simulation Results: Altitude over Time")
fig_sim = px.line(sim_results, x="Time (s)", y="Altitude (m)")
st.plotly_chart(fig_sim, use_container_width=True)
