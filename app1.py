# # Smart Classroom Energy Dashboard
# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns

# # Page config
# st.set_page_config(page_title="Smart Classroom Energy Dashboard", layout="wide")

# # Load dataset
# df = pd.read_csv("iot_energy_data_sample.csv")  # ✅ Ensure file is present in the same directory

# st.title("🏫 Smart Energy Dashboard for Classrooms")

# # Overview Table
# st.subheader("📄 Classroom Energy Consumption Overview")
# st.write(df)

# # Metrics
# avg_energy = df["Total_Energy_kWh_Per_Month"].mean()
# total_energy = df["Total_Energy_kWh_Per_Month"].sum()
# st.metric("⚡ Average Monthly Energy (kWh)", f"{avg_energy:.2f}")
# st.metric("⚡ Total Energy Consumption (kWh)", f"{total_energy:.2f}")

# # Appliance Count vs Energy
# st.subheader("🔌 Appliance Count vs Monthly Energy")

# col1, col2 = st.columns(2)
# with col1:
#     fig_fan, ax_fan = plt.subplots()
#     sns.barplot(data=df, x="Fan_Count", y="Total_Energy_kWh_Per_Month", ax=ax_fan, palette="Blues")
#     ax_fan.set_title("Fan Count vs Energy Usage")
#     st.pyplot(fig_fan)

# with col2:
#     fig_light, ax_light = plt.subplots()
#     sns.barplot(data=df, x="Light_Count", y="Total_Energy_kWh_Per_Month", ax=ax_light, palette="Oranges")
#     ax_light.set_title("Light Count vs Energy Usage")
#     st.pyplot(fig_light)

# # Histogram of Energy Usage
# st.subheader("📊 Distribution of Monthly Energy Consumption")
# fig_hist, ax_hist = plt.subplots()
# sns.histplot(df["Total_Energy_kWh_Per_Month"], kde=True, color="green", bins=10, ax=ax_hist)
# ax_hist.set_title("Distribution of Energy (kWh)")
# st.pyplot(fig_hist)

# # Correlation Heatmap
# st.subheader("📈 Correlation Between Features")
# fig_corr, ax_corr = plt.subplots()
# numeric_df = df.select_dtypes(include=["number"])  # Only numerical columns
# sns.heatmap(numeric_df.corr(), annot=True, cmap="YlGnBu", ax=ax_corr)
# st.pyplot(fig_corr)

# # 💰 Energy Cost Calculation (₹50 per 20 kWh → ₹2.5 per kWh)
# st.subheader("💰 Monthly Energy Cost Summary")
# cost_per_kwh = 2.5  # ₹2.5 per kWh

# # Calculate cost
# df["Monthly_Energy_Cost_Rupee"] = df["Total_Energy_kWh_Per_Month"] * cost_per_kwh
# total_cost_rupee = df["Monthly_Energy_Cost_Rupee"].sum()
# st.metric("💰 Total Monthly Energy Bill (₹)", f"₹{total_cost_rupee:,.2f}")

# # Show cost per classroom
# st.subheader("🏷 Monthly Energy Cost per Classroom (₹)")
# cost_df = df[["Classroom_ID", "Monthly_Energy_Cost_Rupee"]].copy()
# cost_df.rename(columns={"Monthly_Energy_Cost_Rupee": "Monthly_Cost_Rupee"}, inplace=True)
# st.dataframe(cost_df)

# # Plot cost
# fig_cost, ax_cost = plt.subplots(figsize=(10, 4))
# sns.barplot(data=cost_df, x="Classroom_ID", y="Monthly_Cost_Rupee", palette="magma", ax=ax_cost)
# ax_cost.set_ylabel("Cost (₹)")
# ax_cost.set_title("Energy Cost per Classroom")
# st.pyplot(fig_cost)

# # Smart Recommendations
# st.subheader("💡 Smart Recommendations")
# recommendations = []

# for _, row in df.iterrows():
#     if row["Total_Energy_kWh_Per_Month"] > 400:
#         msg = f"{row['Classroom_ID']} - High usage! Consider motion sensors or energy-saving fans."
#         st.warning(msg)
#         recommendations.append(msg)
#     elif row["Fan_Count"] >= 8 and row["Light_Count"] >= 4:
#         msg = f"{row['Classroom_ID']} - Consider scheduling appliance usage to avoid overload."
#         st.info(msg)
#         recommendations.append(msg)

# # Download Recommendations
# if recommendations:
#     st.download_button("📥 Download Recommendations", "\n".join(recommendations), "recommendations.txt")

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(page_title="Fan & Light Energy Cost Calculator", layout="centered")
st.title("🌀💡 1-Hour Fan & Light Energy & Cost Calculator")

# Constants
fan_power_watt = 25       # 25 W per fan
light_power_watt = 40     # 40 W per light
usage_hours = 1           # 1 hour

# Inputs
fan_count   = st.number_input("Enter number of fans:",   min_value=0, step=1, value=6)
light_count = st.number_input("Enter number of lights:", min_value=0, step=1, value=4)
rate        = st.number_input("Enter electricity rate per unit (₹/kWh):",
                              min_value=0.0, value=2.5, step=0.1)

# Calculations
energy_per_fan_kwh   = fan_power_watt   * usage_hours / 1000
energy_per_light_kwh = light_power_watt * usage_hours / 1000

total_energy_fans   = energy_per_fan_kwh   * fan_count
total_energy_lights = energy_per_light_kwh * light_count
total_energy        = total_energy_fans + total_energy_lights

cost_per_fan   = energy_per_fan_kwh   * rate
cost_per_light = energy_per_light_kwh * rate

total_cost_fans   = cost_per_fan   * fan_count
total_cost_lights = cost_per_light * light_count
total_cost        = total_cost_fans + total_cost_lights

# Outputs
st.markdown("### 🔍 Results")
st.info   (f"⚡ Energy — Fans: {total_energy_fans:.3f} kWh, Lights: {total_energy_lights:.3f} kWh")
st.success(f"💸 Cost   — Fans: ₹{total_cost_fans:.2f}, Lights: ₹{total_cost_lights:.2f}")
st.metric("💡 Total Energy (kWh)", f"{total_energy:.3f}")
st.metric("💰 Total Cost (₹)", f"₹{total_cost:.2f}")

# 1️⃣ BAR CHART: Energy per Appliance
st.subheader("📊 Energy per Appliance (kWh)")
bar_df = pd.DataFrame({
    "Appliance": ["Fans", "Lights"],
    "Energy_kWh": [total_energy_fans, total_energy_lights]
})
fig1, ax1 = plt.subplots()
ax1.bar(bar_df["Appliance"], bar_df["Energy_kWh"], color=["skyblue","gold"])
ax1.set_ylabel("Energy (kWh)")
ax1.set_title("Energy Used in 1 Hour")
st.pyplot(fig1)

# 2️⃣ PIE CHART: Cost Share
st.subheader("🥧 Cost Share per Appliance")
fig2, ax2 = plt.subplots()
ax2.pie([total_cost_fans, total_cost_lights],
        labels=["Fans", "Lights"],
        autopct="%1.1f%%",
        startangle=140)
ax2.set_title("Cost Distribution")
st.pyplot(fig2)

# 3️⃣ LINE CHART: Cost vs Count
st.subheader("📈 Cost vs Number of Units")
line_df = pd.DataFrame({
    "Count": list(range(1, 11)),
    "Fan Cost":   [i * cost_per_fan   for i in range(1, 11)],
    "Light Cost": [i * cost_per_light for i in range(1, 11)]
})
fig3, ax3 = plt.subplots()
ax3.plot(line_df["Count"], line_df["Fan Cost"],   marker="o", label="Fans")
ax3.plot(line_df["Count"], line_df["Light Cost"], marker="s", label="Lights")
ax3.set_xlabel("Number of Units")
ax3.set_ylabel("Cost (₹)")
ax3.set_title("Cost vs Number of Fans/Lights")
ax3.legend()
st.pyplot(fig3)