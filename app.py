 

# Steps for Todays Project
# 1.Basic code shared below.. Candidates can add more features like user authentication, advanced analytics, or real-time data updates.
# 2.Improve the UI/UX of the dashboard for better user engagement.
# 3.Use Render to Upload the Project 
# 4.Upload Project on GitHub https://github.com/yourusername/your-repo
# 
# Project
# Smart Energy Consumption Dashboard (Additional Enhancement to be made my candidates)
# import all the libraries

import streamlit as st  # Frontend framework for building web apps
import pandas as pd     # Data manipulation and analysis
import matplotlib.pyplot as plt  # Data visualization
import seaborn as sns  # Statistical data visualization

# Step 1: Load dataset
# Load dataset
df = pd.read_csv("energy_data_india.csv")

st.title("Energy Dashboard for Housing Complex")

# Step 2: Create Sidebar Filters
# Sidebar Filters
region = st.sidebar.selectbox("Select Region", ["All"] + sorted(df["Region"].unique().tolist()))

if region != "All":
    df = df[df["Region"] == region]

st.subheader(" Household Energy Consumption Overview")
st.write(df.head())

# Step 3: Metrics
avg_energy = df["Monthly_Energy_Consumption_kWh"].mean()
total_energy = df["Monthly_Energy_Consumption_kWh"].sum()
st.metric("Average Monthly Consumption (kWh)", f"{avg_energy:.2f}")
st.metric("Total Energy Consumption (kWh)", f"{total_energy:.0f}")

# Step 4: Visualizations
# Energy vs Income
st.subheader(" Income vs Energy Consumption")
fig1, ax1 = plt.subplots()
sns.scatterplot(data=df, x="Monthly_Income_INR", y="Monthly_Energy_Consumption_kWh", hue="Region", ax=ax1)
st.pyplot(fig1)

# Appliance Contribution
st.subheader(" Appliance-wise Count vs Energy Consumption")
appliances = ["Appliance_AC", "Appliance_Fan", "Appliance_Light", "Fridge", "Washing_Machine", "EV_Charging"]
selected_appliance = st.selectbox("Select Appliance", appliances)
fig2, ax2 = plt.subplots()
sns.barplot(x=df[selected_appliance], y=df["Monthly_Energy_Consumption_kWh"], ax=ax2)
ax2.set_xlabel(f"No. of {selected_appliance.replace('_', ' ')}")
ax2.set_ylabel("Energy Consumption (kWh)")
st.pyplot(fig2)

# Step 5: Recommendations
st.subheader(" Smart Recommendations")
for _, row in df.iterrows():
    if row["Monthly_Energy_Consumption_kWh"] > 250:
        st.warning(f"Household ID {row['Household_ID']} - High usage! Recommend switching to solar and LED bulbs.")
    elif row["EV_Charging"] == 1:
        st.info(f"Household ID {row['Household_ID']} - Consider installing a separate EV meter for optimal billing.")

# Step 6: Download Recommendations
# For Candidates Create a download link for the recommendations
recommendations = []
for _, row in df.iterrows():
    if row["Monthly_Energy_Consumption_kWh"] > 250:
        recommendations.append(f"Household ID {row['Household_ID']} - High usage! Recommend switching to solar and LED bulbs.")
    elif row["EV_Charging"] == 1:
        recommendations.append(f"Household ID {row['Household_ID']} - Consider installing a separate EV meter for optimal billing.")

if recommendations:
    st.download_button("Download Recommendations", "\n".join(recommendations), "recommendations.txt")

# Step 7: Conclusion to be added by Candidates
# Candidates can add More :: CSS, Graphs, ML models

#
