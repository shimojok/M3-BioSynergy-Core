import streamlit as st
import pandas as pd

from core_model import run_soil_carbon_model
from mrv import compare_model_vs_observed, generate_mrv_report
from planetary_os_adapter import export_soil_module_state

# -----------------------
# Language dictionary
# -----------------------
LANG = {
    "en": {
        "page_title": "Soil–Carbon–Finance Dashboard",
        "title": "🌍 Soil–Carbon–Finance Dashboard",
        "caption": "Baseline vs MBT55 Project Scenario",
        "sidebar_common": "Common Parameters",
        "sidebar_scenario": "Scenario Settings",
        "years": "Simulation Years",
        "area": "Project Area (ha)",
        "initial_soc": "Initial SOC (tC/ha)",
        "carbon_price": "Carbon Credit Price (USD/tCO₂e)",
        "yield_baseline": "Baseline Yield (t/ha)",
        "yield_price": "Crop Price (USD/t)",
        "mbt_dose": "MBT55 Application Level (Project)",
        "tab_overview": "📊 Overview",
        "tab_soil": "🦠 Soil & Microbes",
        "tab_carbon": "🌿 Carbon",
        "tab_finance": "💰 Green Premium",
        "tab_mrv": "📑 MRV",
        "tab_export": "🚀 Export",
        "overview_sub": "Summary: Baseline vs MBT55",
        "metric_additional_seq": "Additional Sequestration (tCO₂e/ha)",
        "metric_carbon_rev": "Carbon Credit Revenue (USD/yr, Total Project)",
        "metric_total_gp": "Total Green Premium (USD/yr)",
        "overview_carbon_title": "Carbon Sequestration: Baseline vs MBT55",
        "overview_additional_title": "Additional Sequestration (MBT55 - Baseline)",
        "soil_sub": "Soil Carbon Stock: Baseline vs MBT55",
        "soil_ecology": "Soil Ecology (Microbes, Substrate, Stability)",
        "carbon_sub": "Annual Carbon Sequestration Flow",
        "finance_sub": "Green Premium Breakdown",
        "finance_carbon": "Carbon Credit Revenue",
        "finance_yield": "Yield Improvement Revenue",
        "finance_total": "Total Green Premium",
        "finance_note": "Note: Simplified model. Real projects require MRV, leakage, and additionality assessment.",
        "mrv_header": "📑 MRV (Measurement, Reporting, Verification)",
        "mrv_upload_title": "Upload Observed Data",
        "mrv_upload_label": "Upload CSV or Excel",
        "mrv_loaded": "Data loaded successfully.",
        "mrv_metrics": "Metrics",
        "mrv_rmse_soc": "RMSE (SOC)",
        "mrv_bias_soc": "Bias (SOC)",
        "mrv_r2_soc": "R² (SOC)",
        "mrv_rmse_flux": "RMSE (Flux)",
        "mrv_rmse_yield": "RMSE (Yield)",
        "mrv_report_title": "MRV Report (JSON)",
        "mrv_load_error": "Data load error",
        "export_header": "🚀 Planetary OS Export",
        "export_sub": "Soil Module State (Planetary OS Format)",
        "export_caption": "Standardized format for Planetary OS Core integration.",
        "lang_ja": "日本語",
        "lang_en": "English",
    },
    "ja": {
        "page_title": "Soil–Carbon–Finance Dashboard",
        "title": "🌍 Soil–Carbon–Finance Dashboard",
        "caption": "現状 vs MBT55 導入後の差分を可視化",
        "sidebar_common": "共通パラメータ",
        "sidebar_scenario": "シナリオ設定",
        "years": "シミュレーション年数",
        "area": "プロジェクト面積 (ha)",
        "initial_soc": "初期土壌炭素ストック (tC/ha)",
        "carbon_price": "カーボンクレジット単価 (USD/tCO₂e)",
        "yield_baseline": "基準収量 (t/ha)",
        "yield_price": "作物単価 (USD/t)",
        "mbt_dose": "MBT55 導入強度（プロジェクト）",
        "tab_overview": "📊 Overview",
        "tab_soil": "🦠 土壌・微生物",
        "tab_carbon": "🌿 炭素隔離",
        "tab_finance": "💰 グリーンプレミアム",
        "tab_mrv": "📑 MRV",
        "tab_export": "🚀 Export",
        "overview_sub": "現状 vs MBT55 導入後：サマリー",
        "metric_additional_seq": "追加隔離量 (合計, tCO₂e/ha)",
        "metric_carbon_rev": "カーボンクレジット収益 (USD/yr, プロジェクト全体)",
        "metric_total_gp": "総グリーンプレミアム (USD/yr)",
        "overview_carbon_title": "炭素隔離：Baseline vs MBT55",
        "overview_additional_title": "追加隔離量（MBT55 - Baseline）",
        "soil_sub": "土壌炭素ストック：Baseline vs MBT55",
        "soil_ecology": "土壌生態（微生物・基質・安定性）",
        "carbon_sub": "炭素隔離フロー（年次）",
        "finance_sub": "グリーンプレミアム内訳",
        "finance_carbon": "カーボンクレジット収益",
        "finance_yield": "収量向上による収益",
        "finance_total": "総グリーンプレミアム",
        "finance_note": "※ 単純化した試算モデル。実際のプロジェクトでは MRV・リーケージ・追加性等の精緻化が必要。",
        "mrv_header": "📑 MRV（Measurement, Reporting, Verification）",
        "mrv_upload_title": "実測データのアップロード",
        "mrv_upload_label": "CSV または Excel をアップロード",
        "mrv_loaded": "データを読み込みました。",
        "mrv_metrics": "指標",
        "mrv_rmse_soc": "RMSE (SOC)",
        "mrv_bias_soc": "Bias (SOC)",
        "mrv_r2_soc": "R² (SOC)",
        "mrv_rmse_flux": "RMSE (Flux)",
        "mrv_rmse_yield": "RMSE (Yield)",
        "mrv_report_title": "MRV レポート（JSON）",
        "mrv_load_error": "データ読み込みエラー",
        "export_header": "🚀 Planetary OS Export",
        "export_sub": "Soil Module State (Planetary OS Format)",
        "export_caption": "Planetary OS Core に渡すための標準化フォーマット。",
        "lang_ja": "日本語",
        "lang_en": "English",
    },
}

# -----------------------
# Language toggle
# -----------------------
if "lang" not in st.session_state:
    st.session_state["lang"] = "en"

lang_col1, lang_col2 = st.columns(2)
with lang_col1:
    if st.button(LANG[st.session_state["lang"]]["lang_ja"]):
        st.session_state["lang"] = "ja"
with lang_col2:
    if st.button(LANG[st.session_state["lang"]]["lang_en"]):
        st.session_state["lang"] = "en"

L = LANG[st.session_state["lang"]]

# -----------------------
# Page config & title
# -----------------------
st.set_page_config(page_title=L["page_title"], layout="wide")
st.title(L["title"])
st.caption(L["caption"])

# -----------------------
# Sidebar: Common Parameters
# -----------------------
st.sidebar.header(L["sidebar_common"])

years = st.sidebar.slider(L["years"], 5, 30, 15)
area_ha = st.sidebar.number_input(L["area"], 1.0, 1_000_000.0, 765.0, step=1.0)
initial_soc = st.sidebar.number_input(L["initial_soc"], 10.0, 200.0, 50.0, step=1.0)

carbon_price = st.sidebar.number_input(L["carbon_price"], 10.0, 500.0, 210.0, step=10.0)
yield_baseline = st.sidebar.number_input(L["yield_baseline"], 1.0, 20.0, 7.7, step=0.1)
yield_price = st.sidebar.number_input(L["yield_price"], 50.0, 2000.0, 500.0, step=10.0)

# -----------------------
# Scenario Settings
# -----------------------
st.sidebar.header(L["sidebar_scenario"])

mbt_dose_project = st.sidebar.slider(L["mbt_dose"], 0.0, 3.0, 1.5, step=0.1)

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
    [
        L["tab_overview"],
        L["tab_soil"],
        L["tab_carbon"],
        L["tab_finance"],
        L["tab_mrv"],
        L["tab_export"],
    ]
)

# -----------------------
# Overview
# -----------------------
with tab_overview:
    st.subheader(L["overview_sub"])

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            L["metric_additional_seq"],
            f"{total_additional_sequestration_per_ha:.2f}",
        )
    with col2:
        st.metric(
            L["metric_carbon_rev"],
            f"{annual_green_premium_carbon_total:,.0f}",
        )
    with col3:
        st.metric(
            L["metric_total_gp"],
            f"{total_green_premium:,.0f}",
        )

    st.markdown(f"### {L['overview_carbon_title']}")
    chart_df = pd.DataFrame({
        "Year": df_baseline["year"],
        "Baseline (tCO₂e/ha/yr)": df_baseline["sequestration_tco2e_ha_yr"],
        "MBT55 (tCO₂e/ha/yr)": df_project["sequestration_tco2e_ha_yr"],
    }).set_index("Year")
    st.line_chart(chart_df)

    st.markdown(f"### {L['overview_additional_title']}")
    st.area_chart(df_diff.set_index("year")[["sequestration_diff"]])

# -----------------------
# Soil
# -----------------------
with tab_soil:
    st.subheader(L["soil_sub"])
    soil_df = pd.DataFrame({
        "Year": df_baseline["year"],
        "SOC Baseline (tC/ha)": df_baseline["soc_tC_ha"],
        "SOC MBT55 (tC/ha)": df_project["soc_tC_ha"],
    }).set_index("Year")
    st.line_chart(soil_df)

    st.markdown(f"### {L['soil_ecology']}")
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
    st.subheader(L["carbon_sub"])
    st.line_chart(chart_df)

# -----------------------
# Finance
# -----------------------
with tab_finance:
    st.subheader(L["finance_sub"])

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"#### {L['finance_carbon']}")
        st.write(f"Additional sequestration: **{total_additional_sequestration_per_ha:.2f} tCO₂e/ha/yr**")
        st.write(f"Price: **{carbon_price:.0f} USD/tCO₂e**")
        st.write(f"Revenue (per ha): **{annual_green_premium_carbon:.0f} USD/ha/yr**")
        st.write(f"Total project: **{annual_green_premium_carbon_total:,.0f} USD/yr**")

    with col2:
        st.markdown(f"#### {L['finance_yield']}")
        st.write(f"Baseline yield (avg): **{df_baseline['yield_t_ha'].mean():.2f} t/ha**")
        st.write(f"Project yield (avg): **{df_project['yield_t_ha'].mean():.2f} t/ha**")
        st.write(f"Difference (avg): **{df_diff['yield_diff'].mean():.2f} t/ha**")
        st.write(f"Revenue: **{annual_green_premium_yield:,.0f} USD/yr**")

    st.markdown(f"#### {L['finance_total']}")
    st.write(f"**{total_green_premium:,.0f} USD/yr**")
    st.caption(L["finance_note"])

# -----------------------
# MRV
# -----------------------
with tab_mrv:
    st.header(L["mrv_header"])

    st.markdown(f"### {L['mrv_upload_title']}")
    uploaded_file = st.file_uploader(L["mrv_upload_label"], type=["csv", "xlsx"])

    if uploaded_file:
        try:
            if uploaded_file.name.endswith(".csv"):
                obs_df = pd.read_csv(uploaded_file)
            else:
                obs_df = pd.read_excel(uploaded_file)

            st.success(L["mrv_loaded"])
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

            st.markdown(f"### {L['mrv_metrics']}")
            st.write(f"**{L['mrv_rmse_soc']}**:", stats.get("rmse_soc"))
            st.write(f"**{L['mrv_bias_soc']}**:", stats.get("bias_soc"))
            st.write(f"**{L['mrv_r2_soc']}**:", stats.get("r2_soc"))
            st.write(f"**{L['mrv_rmse_flux']}**:", stats.get("rmse_flux"))
            st.write(f"**{L['mrv_rmse_yield']}**:", stats.get("rmse_yield"))

            st.markdown(f"### {L['mrv_report_title']}")
            report = generate_mrv_report(model_for_mrv, obs_for_mrv, stats)
            st.json(report)

        except Exception as e:
            st.error(f"{L['mrv_load_error']}: {e}")

# -----------------------
# Export
# -----------------------
with tab_export:
    st.header(L["export_header"])

    st.markdown(f"### {L['export_sub']}")

    export_data = export_soil_module_state(
        df_baseline,
        df_project,
        {**common_params, "mbt_dose": mbt_dose_project},
    )

    st.json(export_data)
    st.caption(L["export_caption"])
