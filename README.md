# Candidate Name - Ariella Sansita M

# Candidate Registration Number - 1000470

# CRS Name: Artificial Intelligence

# Course Name - Mathematics for AI

# School name - Birla Open Minds International School, Kollur

# Summative Assessment

# Rocket Launch

## Project Overview

This project is an interactive Streamlit dashboard that analyzes historical space mission data and includes a calculus-based rocket launch simulation. The goal is to explore relationships between payload weight, fuel consumption, mission cost, crew size, mission duration, and mission success. In addition, a physics simulation models rocket motion using Newton’s Second Law and step-by-step numerical updates. The dashboard allows users to filter mission data and experiment with rocket parameters in real time.


## Problem Understanding

Rocket launches are governed primarily by:

- Thrust (upward force from engines)
- Gravity (downward force due to Earth's pull)
- Variable mass (fuel burn reduces mass over time)

As fuel burns, total mass decreases. Since acceleration depends on force divided by mass, the rocket accelerates differently over time.

This project investigates:

- How payload weight affects fuel consumption
- Whether mission cost relates to mission success
- How mission duration relates to distance from Earth
- What thrust level is required for successful lift-off


## Data Preprocessing & Cleaning

The dataset was processed using Pandas to ensure accuracy:

- Removed extra spaces from column names
- Converted "Launch Date" to datetime format
- Converted numeric columns (mission cost, fuel, payload, duration, etc.) to numeric types
- Removed rows containing missing values
- Created a binary mission status (Success/Failure) based on Mission Success (%)

Exploratory checks were performed using `.head()`, `.info()`, and numeric conversion validation.


## Interactive Dashboard Features

Users can filter the dataset using:

- Mission Type dropdown
- Launch Vehicle dropdown
- Mission Cost range slider

If filters result in no matching missions, the app safely displays a warning instead of crashing.


## Data Visualizations

The dashboard includes the following visualizations:

### 1. Payload Weight vs Fuel Consumption (Scatter Plot)
Shows the relationship between payload mass and required fuel.

**Insight:** Heavier payloads generally require greater fuel consumption.


### 2. Average Mission Cost: Success vs Failure (Bar Chart)
Compares average cost between missions classified as success (≥ 80%) and failure.

**Insight:** Higher cost does not automatically guarantee success.


### 3. Crew Size Distribution by Mission Status (Box Plot)
Analyzes variation in crew size between successful and failed missions.

**Insight:** Successful missions tend to show consistent crew ranges, while failures may show greater variability.


### 4. Mission Duration vs Distance from Earth (Line Chart)
Displays how mission duration changes with increasing distance.

**Insight:** Greater travel distance is associated with longer mission duration.


### 5. Correlation Heatmap
Displays statistical relationships between all numeric variables.

**Insight:** Strong positive correlations exist between payload weight and fuel consumption.


## Rocket Launch Simulation

The simulation models rocket motion using Newton’s Second Law:

F = m × a  

Net Force is calculated as:

F_net = Thrust − (Mass × g)

Where:
- g = 9.81 m/s²
- Mass = Dry Mass + Remaining Fuel

The system is solved using Euler’s Method with 1-second time steps:

v_new = v_old + a × Δt  
h_new = h_old + v × Δt  

Fuel decreases each second using a constant burn rate.  
If fuel is depleted, only gravity acts on the rocket.

The simulation stores time, altitude, velocity, and remaining fuel and visualizes altitude over time.


## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Plotly
- Streamlit

## How to Run Locally

Install required packages:

pip install -r requirements.txt  

Run the app:

streamlit run app.py  


## Live Application

https://rocket-launch-7sbol2huxgtgljnggyjcez.streamlit.app/


