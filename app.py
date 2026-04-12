import sys
import subprocess
# 強制的にAltairをインストール
try:
    import altair
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--force-reinstall", "altair"])
    import altair
import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="Soil–Carbon–Finance Dashboard", layout="wide")
st.title("🌍 Soil Ecology × Carbon Sequestration × Green Premium")

# -----------------------------
# Sidebar: Scenario parameters
# -----------------------------
st.sidebar.header("⚙️ Scenario Settings")

area_ha = st.sidebar.slider("対象面積 (ha)", 1.0, 1000.0, 100.0, 1.0)
mbt_dose = st.sidebar.slider("MBT55 投入強度 (相対値)", 0.0, 3.0, 1.0, 0.1)
management = st.sidebar.selectbox("土壌生態制御レベル", ["慣行", "中強度再生", "高強度再生"])

carbon_price = st.sidebar.slider("カーボンクレジット価格 (USD/tCO₂e)", 10, 300, 80, 5)
yield_baseline = st.sidebar.slider("基準収量 (t/ha)", 1.0, 15.0, 5.0, 0.1)
yield_uplift_pct = st.sidebar.slider("収量向上率 (%)", 0.0, 50.0, 15.0, 1.0)
price_per_ton = st.sidebar.slider("作物販売価格 (USD/t)", 100, 2000, 500, 50)

# 管理レベルによる係数
if management == "慣行":
    soil_factor = 1.0
    sequestration_factor = 0.5
    nitro_loss_factor = 1.0
elif management == "中強度再生":
    soil_factor = 1.5
    sequestration_factor = 1.5
    nitro_loss_factor = 0.7
else:  # 高強度再生
    soil_factor = 2.2
    sequestration_factor = 2.5
    nitro_loss_factor = 0.5

# MBT55 の効果を掛け合わせ
soil_factor *= (1 + 0.3 * mbt_dose)
sequestration_factor *= (1 + 0.4 * mbt_dose)
nitro_loss_factor *= max(0.2, 1 - 0.2 * mbt_dose)

years = np.arange(0, 21)

# -----------------------------
# Soil ecology model (toy)
# -----------------------------
def simulate_soil_ecology():
    microbes = 0.8 * soil_factor
    substrate = 1.0
    stability = 0.3 + 0.1 * soil_factor

    data = {"Year": [], "Microbial Biomass": [], "Substrate": [], "Soil Stability": []}
    for t in years:
        microbes = microbes + 0.05 * microbes * (substrate) - 0.01 * microbes
        substrate = max(0.1, substrate - 0.03 * microbes + 0.05 * soil_factor)
        stability = min(1.0, stability + 0.01 * soil_factor)

        data["Year"].append(t)
        data["Microbial Biomass"].append(microbes)
        data["Substrate"].append(substrate)
        data["Soil Stability"].append(stability)
    return pd.DataFrame(data)

# -----------------------------
# C / N cycle model (toy)
# -----------------------------
def simulate_CN_cycles():
    soil_C = 40.0  # tC/ha
    soil_N = 3.0   # tN/ha
    N_loss = 0.08 * nitro_loss_factor

    data = {"Year": [], "Soil C (tC/ha)": [], "Soil N (tN/ha)": [], "N Loss (tN/ha/yr)": []}
    for t in years:
        soil_C = soil_C + 0.6 * sequestration_factor - 0.2
        soil_N = soil_N + 0.05 * soil_factor - N_loss
        data["Year"].append(t)
        data["Soil C (tC/ha)"].append(soil_C)
        data["Soil N (tN/ha)"].append(soil_N)
        data["N Loss (tN/ha/yr)"].append(N_loss)
    return pd.DataFrame(data)

# -----------------------------
# Carbon sequestration & GHG
# -----------------------------
def simulate_carbon_sequestration():
    # tCO2e/ha/yr
    annual_sequestration = 2.0 * sequestration_factor
    baseline_sequestration = 0.5
    net_additional = annual_sequestration - baseline_sequestration

    data = {"Year": [], "Baseline (tCO2e/ha/yr)": [], "Project (tCO2e/ha/yr)": [], "Additional (tCO2e/ha/yr)": []}
    for t in years:
        data["Year"].append(t)
        data["Baseline (tCO2e/ha/yr)"].append(baseline_sequestration)
        data["Project (tCO2e/ha/yr)"].append(annual_sequestration)
        data["Additional (tCO2e/ha/yr)"].append(net_additional)
    return pd.DataFrame(data), net_additional

# -----------------------------
# Green premium calculation
# -----------------------------
def compute_green_premium(additional_tCO2e_per_ha):
    # カーボンクレジット収益
    carbon_revenue_per_ha_per_year = additional_tCO2e_per_ha * carbon_price
    carbon_revenue_total = carbon_revenue_per_ha_per_year * area_ha

    # 収量向上による収益
    uplift_yield = yield_baseline * (yield_uplift_pct / 100.0)
    revenue_yield_per_ha = uplift_yield * price_per_ton
    revenue_yield_total = revenue_yield_per_ha * area_ha

    total_green_value = carbon_revenue_total + revenue_yield_total

    return {
        "carbon_revenue_per_ha_per_year": carbon_revenue_per_ha_per_year,
        "carbon_revenue_total": carbon_revenue_total,
        "revenue_yield_per_ha": revenue_yield_per_ha,
        "revenue_yield_total": revenue_yield_total,
        "total_green_value": total_green_value,
    }

# -----------------------------
# Run simulations
# -----------------------------
df_soil = simulate_soil_ecology()
df_cn = simulate_CN_cycles()
df_sequestration, add_tCO2e = simulate_carbon_sequestration()
gp = compute_green_premium(add_tCO2e)

# -----------------------------
# Layout
# -----------------------------
tab_overview, tab_soil, tab_cn, tab_carbon, tab_finance = st.tabs(
    ["📊 Overview", "🦠 Soil Ecology", "🔁 C / N Cycles", "🌿 Carbon Sequestration", "💰 Green Premium"]
)

# -----------------------------
# Overview
# -----------------------------
with tab_overview:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("追加炭素隔離量 (tCO₂e/ha/yr)", f"{add_tCO2e:.2f}")
        st.metric("カーボンクレジット収益 (USD/ha/yr)", f"{gp['carbon_revenue_per_ha_per_year']:.0f}")
    with col2:
        st.metric("収量向上収益 (USD/ha/yr)", f"{gp['revenue_yield_per_ha']:.0f}")
        st.metric("総グリーン価値 (USD/yr)", f"{gp['total_green_value']:.0f}")
    with col3:
        st.metric("土壌安定性 (最終年)", f"{df_soil['Soil Stability'].iloc[-1]:.2f}")
        st.metric("土壌炭素ストック (tC/ha, 最終年)", f"{df_cn['Soil C (tC/ha)'].iloc[-1]:.1f}")

    st.subheader("追加炭素隔離プロファイル")

# 152行目の前に追加
import sys
print("Python executable:", sys.executable)
print("Python path:", sys.path)

try:
    import altair as alt
    print("Altair imported successfully. Version:", alt.__version__)
except ImportError as e:
    print(f"Altair import failed: {e}")
    st.error(f"Altair not available: {e}")
    # フォールバック：matplotlibを使用
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    df_sequestration.set_index("Year")[["Baseline (tCO2e/ha/yr)", "Project (tCO2e/ha/yr)"]].plot(ax=ax)
    st.pyplot(fig)
    st.stop()

# 元の152行目
st.area_chart(df_sequestration.set_index("Year")[["Baseline (tCO2e/ha/yr)", "Project (tCO2e/ha/yr)"]])

# -----------------------------
# Soil Ecology
# -----------------------------
with tab_soil:
    st.subheader("土壌生態制御：微生物・基質・安定性")
    col1, col2 = st.columns(2)
    with col1:
        st.line_chart(df_soil.set_index("Year")[["Microbial Biomass"]])
        st.line_chart(df_soil.set_index("Year")[["Substrate"]])
    with col2:
        st.line_chart(df_soil.set_index("Year")[["Soil Stability"]])

# -----------------------------
# C / N Cycles
# -----------------------------
with tab_cn:
    st.subheader("炭素・窒素循環プロファイル")
    col1, col2 = st.columns(2)
    with col1:
        st.line_chart(df_cn.set_index("Year")[["Soil C (tC/ha)"]])
    with col2:
        st.line_chart(df_cn.set_index("Year")[["Soil N (tN/ha)"]])
        st.line_chart(df_cn.set_index("Year")[["N Loss (tN/ha/yr)"]])

# -----------------------------
# Carbon Sequestration
# -----------------------------
with tab_carbon:
    st.subheader("炭素隔離と追加性 (Additionality)")
    st.line_chart(df_sequestration.set_index("Year"))
    st.caption("Baseline vs Project vs Additional (tCO₂e/ha/yr)")

# -----------------------------
# Green Premium
# -----------------------------
with tab_finance:
    st.subheader("グリーンプレミアム算出")
    col1, col2 = st.columns(2)
    with col1:
        st.write("**カーボンクレジット収益**")
        st.write(f"- 追加隔離量: {add_tCO2e:.2f} tCO₂e/ha/yr")
        st.write(f"- 単価: {carbon_price} USD/tCO₂e")
        st.write(f"- 収益: {gp['carbon_revenue_per_ha_per_year']:.0f} USD/ha/yr")
        st.write(f"- プロジェクト全体: {gp['carbon_revenue_total']:.0f} USD/yr")
    with col2:
        st.write("**収量向上による収益**")
        st.write(f"- 基準収量: {yield_baseline:.2f} t/ha")
        st.write(f"- 向上率: {yield_uplift_pct:.1f} %")
        st.write(f"- 収益: {gp['revenue_yield_per_ha']:.0f} USD/ha/yr")
        st.write(f"- プロジェクト全体: {gp['revenue_yield_total']:.0f} USD/yr")

    st.markdown("---")
    st.write(f"**総グリーンプレミアム (カーボン + 収量向上): {gp['total_green_value']:.0f} USD/yr**")
    st.caption("※ 単純化した試算モデル。実際のプロジェクトでは MRV・リーケージ・追加性等の精緻化が必要。")

st.success("Soil–Carbon–Finance Dashboard Loaded.")