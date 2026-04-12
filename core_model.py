import numpy as np
import pandas as pd


def run_soil_carbon_model(params: dict) -> dict:
    """
    土壌炭素・炭素隔離・収量・土壌生態・C/N をまとめて計算する簡易モデル（拡張版）。

    params 例:
        years: int
        area_ha: float
        initial_soc: float (tC/ha)
        carbon_price: float
        yield_baseline: float (t/ha)
        yield_price: float
        mbt_dose: float (0–3)
    """
    years = int(params.get("years", 15))
    initial_soc = float(params.get("initial_soc", 50.0))
    mbt_dose = float(params.get("mbt_dose", 0.0))
    yield_baseline = float(params.get("yield_baseline", 7.7))

    # タイム軸
    t = np.arange(1, years + 1)

    # --- MBT55 / 再生度合いによる係数（かなり単純化した形） ---
    # 土壌生態
    soil_factor = 1.0 + 0.4 * mbt_dose
    sequestration_factor = 1.0 + 0.6 * mbt_dose
    nitro_loss_factor = max(0.3, 1.0 - 0.25 * mbt_dose)

    # --- SOC ダイナミクス ---
    soc = np.zeros_like(t, dtype=float)
    soc[0] = initial_soc
    for i in range(1, years):
        # 年次の炭素流入（tC/ha/yr）
        c_input = 1.2 * soil_factor
        # 分解・損失
        c_loss = 0.8
        soc[i] = soc[i - 1] + c_input * sequestration_factor - c_loss

    # --- 炭素隔離フロー（tCO2e/ha/yr） ---
    # 1 tC = 3.667 tCO2
    soc_delta = np.diff(np.concatenate([[initial_soc], soc]))
    sequestration_tco2e_ha_yr = soc_delta * 3.667

    # --- 収量（t/ha） ---
    # MBT55 による収量向上（単純な線形）
    yield_uplift_pct = 0.1 + 0.15 * mbt_dose  # 10–55% 程度
    yield_t_ha = yield_baseline * (1.0 + yield_uplift_pct) * np.ones_like(t, dtype=float)

    # --- 土壌生態（微生物・基質・安定性） ---
    microbial_biomass = np.zeros_like(t, dtype=float)
    substrate = np.zeros_like(t, dtype=float)
    soil_stability = np.zeros_like(t, dtype=float)

    microbes = 0.8 * soil_factor
    sub = 1.0
    stability = 0.3 + 0.1 * soil_factor

    for i, _ in enumerate(t):
        microbes = microbes + 0.05 * microbes * (sub) - 0.01 * microbes
        sub = max(0.1, sub - 0.03 * microbes + 0.05 * soil_factor)
        stability = min(1.0, stability + 0.01 * soil_factor)

        microbial_biomass[i] = microbes
        substrate[i] = sub
        soil_stability[i] = stability

    # --- C/N サイクル ---
    soil_n = np.zeros_like(t, dtype=float)
    n_loss = np.zeros_like(t, dtype=float)

    n_stock = 3.0  # tN/ha
    base_n_loss = 0.08 * nitro_loss_factor

    for i, _ in enumerate(t):
        n_stock = n_stock + 0.05 * soil_factor - base_n_loss
        soil_n[i] = n_stock
        n_loss[i] = base_n_loss

    return {
        "year": t,
        "soc_tC_ha": soc,
        "sequestration_tco2e_ha_yr": sequestration_tco2e_ha_yr,
        "yield_t_ha": yield_t_ha,
        "microbial_biomass": microbial_biomass,
        "substrate": substrate,
        "soil_stability": soil_stability,
        "soil_n_tN_ha": soil_n,
        "n_loss_tN_ha_yr": n_loss,
    }
