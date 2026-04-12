import streamlit as st
import pandas as pd

from core_model import run_soil_carbon_model
from mrv import compare_model_vs_observed, generate_mrv_report
from planetary_os_adapter import export_soil_module_state

st.set_page_config(page_title="Soil–Carbon–Finance Dashboard (EN)", layout="wide")

st.title("🌍 Soil–Carbon–Finance Dashboard")
st.caption("Baseline vs MBT55 Project Scenario")

# -----------------------
# Sidebar: Common Parameters
# -----------------------
st.sidebar.header("Common Parameters")

years = st.sidebar.slider("Simulation Years", 5, 30, 15)
area_ha = st.sidebar.number_input("Project Area (ha)", 1.0, 1_000_000.0, 765.0, step=1.0)
initial_soc = st.sidebar.number_input("Initial SOC (tC/ha)", 10.0, 200.0, 50.0, step=1.0)

carbon_price = st.sidebar.number_input("Carbon Credit Price (USD/tCO₂e)", 10.0, 500.0, 210.0, step=10.0)
yield_baseline = st.sidebar.number_input("Baseline Yield (t/ha)", 1.0, 20.0, 7.7, step=0.1)
yield_price = st.sidebar.number_input("Crop Price (USD/t)", 50.0, 2000.0, 500.0, step=10.0)

# -----------------------
# Scenario Settings
# -----------------------
st.sidebar.header("Scenario Settings")

mbt_dose_project = st.sidebar.slider("MBT55 Application Level (Project)", 0.0, 3.0, 1.5, step=0.1)

common_params = dict(
    years=years,
    area_ha=area_ha,
    initial_soc=initial_soc,
    carbon_price=carbon_price,
    yield_baseline=yield_baseline,
    yield_price=yield_price,
)

baseline_params = {**common_params, "mbt_dose": 0.0}
project_params = {**common_params, "mbt_dose": mbt_dose_project}

# -----------------------
# Run Model
# -----------------------
baseline = run_soil_carbon_model(baseline_params)
project = run_soil_carbon_model(project_params)

df_baseline = pd.DataFrame(baseline)
df_project = pd.DataFrame(project)

df_diff = df_project.copy()
df_diff["sequestration_diff"] = (
    df_project["sequestration_tco2e_ha_yr"] - df_baseline["sequestration_tco2e_ha_yr"]
)
df_diff["yield_diff"] = df_project["yield_t_ha"] - df_baseline["yield_t_ha"]

# Aggregates
total_additional_sequestration_per_ha = df_diff["sequestration_diff"].sum()
total_additional_sequestration = total_additional_sequestration_per_ha * area_ha

annual_green_premium_carbon = total_additional_sequestration_per_ha * carbon_price
annual_green_premium_carbon_total = annual_green_premium_carbon * area_ha

annual_yield_baseline = df_baseline["yield_t_ha"].mean() * area_ha
annual_yield_project = df_project["yield_t_ha"].mean() * area_ha
annual_yield_diff = annual_yield_project - annual_yield_baseline
annual_green_premium_yield = annual_yield_diff * yield_price

total_green_premium = annual_green_premium_carbon_total + annual_green_premium_yield

# -----------------------
# Layout
# -----------------------
tab_overview, tab_soil, tab_carbon, tab_finance, tab_mrv, tab_export = st.tabs(
    ["📊 Overview", "🦠 Soil & Microbes", "🌿 Carbon", "💰 Green Premium", "📑 MRV", "🚀 Export"]
)

# -----------------------
# Overview
# -----------------------
with tab_overview:
    st.subheader("Summary: Baseline vs MBT55")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            "Additional Sequestration (tCO₂e/ha)",
            f"{total_additional_sequestration_per_ha:.2f}",
        )
    with col2:
        st.metric(
            "Carbon Credit Revenue (USD/yr, Total Project)",
            f"{annual_green_premium_carbon_total:,.0f}",
        )
    with col3:
        st.metric(
            "Total Green Premium (USD/yr)",
            f"{total_green_premium:,.0f}",
        )

    st.markdown("### Carbon Sequestration: Baseline vs MBT55")
    chart_df = pd.DataFrame({
        "Year": df_baseline["year"],
        "Baseline (tCO₂e/ha/yr)": df_baseline["sequestration_tco2e_ha_yr"],
        "MBT55 (tCO₂e/ha/yr)": df_project["sequestration_tco2e_ha_yr"],
    }).set_index("Year")
    st.line_chart(chart_df)

    st.markdown("### Additional Sequestration (MBT55 - Baseline)")
    st.area_chart(df_diff.set_index("year")[["sequestration_diff"]])

# -----------------------
# Soil
# -----------------------
with tab_soil:
    st.subheader("Soil Carbon Stock: Baseline vs MBT55")
    soil_df = pd.DataFrame({
        "Year": df_baseline["year"],
        "SOC Baseline (tC/ha)": df_baseline["soc_tC_ha"],
        "SOC MBT55 (tC/ha)": df_project["soc_tC_ha"],
    }).set_index("Year")
    st.line_chart(soil_df)

    st.markdown("### Soil Ecology (Microbes, Substrate, Stability)")
    col1, col2 = st.columns(2)
    with col1:
        st.line_chart(df_project.set_index("year")[["microbial_biomass"]])
        st.line_chart(df_project.set_index("year")[["substrate"]])
    with col2:
        st.line_chart(df_project.set_index("year")[["soil_stability"]])

# -----------------------
# Carbon
# -----------------------
with tab_carbon:
    st.subheader("Annual Carbon Sequestration Flow")
    st.line_chart(chart_df)

# -----------------------
# Finance
# -----------------------
with tab_finance:
    st.subheader("Green Premium Breakdown")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Carbon Credit Revenue")
        st.write(f"Additional sequestration: **{total_additional_sequestration_per_ha:.2f} tCO₂e/ha/yr**")
        st.write(f"Price: **{carbon_price:.0f} USD/tCO₂e**")
        st.write(f"Revenue (per ha): **{annual_green_premium_carbon:.0f} USD/ha/yr**")
        st.write(f"Total project: **{annual_green_premium_carbon_total:,.0f} USD/yr**")

    with col2:
        st.markdown("#### Yield Improvement Revenue")
        st.write(f"Baseline yield (avg): **{df_baseline['yield_t_ha'].mean():.2f} t/ha**")
        st.write(f"Project yield (avg): **{df_project['yield_t_ha'].mean():.2f} t/ha**")
        st.write(f"Difference (avg): **{df_diff['yield_diff'].mean():.2f} t/ha**")
        st.write(f"Revenue: **{annual_green_premium_yield:,.0f} USD/yr**")

    st.markdown("#### Total Green Premium")
    st.write(f"**{total_green_premium:,.0f} USD/yr**")
    st.caption("Note: Simplified model. Real projects require MRV, leakage, and additionality assessment.")

# -----------------------
# MRV
# -----------------------
with tab_mrv:
    st.header("📑 MRV (Measurement, Reporting, Verification)")

    st.markdown("### Upload Observed Data")
    uploaded_file = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"])

    if uploaded_file:
        try:
            if uploaded_file.name.endswith(".csv"):
                obs_df = pd.read_csv(uploaded_file)
            else:
                obs_df = pd.read_excel(uploaded_file)

            st.success("Data loaded successfully.")
            st.dataframe(obs_df.head())

            model_for_mrv = df_project.rename(
                columns={
                    "soc_tC_ha": "soc_tC_ha_model",
                    "sequestration_tco2e_ha_yr": "sequestration_tco2e_ha_yr_model",
                    "yield_t_ha": "yield_t_ha_model",
                }
            )

            obs_for_mrv = obs_df.rename(
                columns={
                    "soc_tC_ha": "soc_tC_ha_obs",
                    "sequestration_tco2e_ha_yr": "sequestration_tco2e_ha_yr_obs",
                    "yield_t_ha": "yield_t_ha_obs",
                }
            )

            stats = compare_model_vs_observed(model_for_mrv, obs_for_mrv)

            st.markdown("### Metrics")
            st.write("**RMSE (SOC)**:", stats.get("rmse_soc"))
            st.write("**Bias (SOC)**:", stats.get("bias_soc"))
            st.write("**R² (SOC)**:", stats.get("r2_soc"))
            st.write("**RMSE (Flux)**:", stats.get("rmse_flux"))
            st.write("**RMSE (Yield)**:", stats.get("rmse_yield"))

            st.markdown("### MRV Report (JSON)")
            report = generate_mrv_report(model_for_mrv, obs_for_mrv, stats)
            st.json(report)

        except Exception as e:
            st.error(f"Data load error: {e}")

# -----------------------
# Export
# -----------------------
with tab_export:
    st.header("🚀 Planetary OS Export")

    st.markdown("### Soil Module State (Planetary OS Format)")

    export_data = export_soil_module_state(
        df_baseline,
        df_project,
        {**common_params, "mbt_dose": mbt_dose_project},
    )

    st.json(export_data)
    st.caption("Standardized format for Planetary OS Core integration.")
