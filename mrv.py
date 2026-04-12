import pandas as pd
import numpy as np
from typing import Dict


def _safe_merge(model_df: pd.DataFrame, obs_df: pd.DataFrame) -> pd.DataFrame:
    if "year" not in model_df.columns or "year" not in obs_df.columns:
        raise ValueError("MRV 用の比較には 'year' 列が必要です。")
    return pd.merge(model_df, obs_df, on="year", suffixes=("_model", "_obs"))


def _rmse(a, b):
    a = np.array(a, dtype=float)
    b = np.array(b, dtype=float)
    return float(np.sqrt(np.mean((a - b) ** 2)))


def _bias(a, b):
    a = np.array(a, dtype=float)
    b = np.array(b, dtype=float)
    return float(np.mean(a - b))


def _r2(a, b):
    a = np.array(a, dtype=float)
    b = np.array(b, dtype=float)
    ss_res = np.sum((a - b) ** 2)
    ss_tot = np.sum((b - np.mean(b)) ** 2)
    if ss_tot == 0:
        return float("nan")
    return float(1 - ss_res / ss_tot)


def compare_model_vs_observed(
    model_df: pd.DataFrame,
    obs_df: pd.DataFrame,
) -> Dict[str, float]:
    """
    モデル vs 実測の比較指標を計算する。
    - SOC (tC/ha)
    - Flux (tCO2e/ha/yr)
    - Yield (t/ha)
    """
    merged = _safe_merge(model_df, obs_df)

    stats = {}

    if {"soc_tC_ha_model", "soc_tC_ha_obs"}.issubset(merged.columns):
        stats["rmse_soc"] = _rmse(merged["soc_tC_ha_model"], merged["soc_tC_ha_obs"])
        stats["bias_soc"] = _bias(merged["soc_tC_ha_model"], merged["soc_tC_ha_obs"])
        stats["r2_soc"] = _r2(merged["soc_tC_ha_model"], merged["soc_tC_ha_obs"])

    if {
        "sequestration_tco2e_ha_yr_model",
        "sequestration_tco2e_ha_yr_obs",
    }.issubset(merged.columns):
        stats["rmse_flux"] = _rmse(
            merged["sequestration_tco2e_ha_yr_model"],
            merged["sequestration_tco2e_ha_yr_obs"],
        )

    if {"yield_t_ha_model", "yield_t_ha_obs"}.issubset(merged.columns):
        stats["rmse_yield"] = _rmse(
            merged["yield_t_ha_model"], merged["yield_t_ha_obs"]
        )

    return stats


def generate_mrv_report(
    model_df: pd.DataFrame,
    obs_df: pd.DataFrame,
    stats: Dict[str, float],
) -> Dict:
    """
    MRV レポート（JSON）を生成する。
    """
    report = {
        "summary": {
            "rmse_soc": stats.get("rmse_soc"),
            "bias_soc": stats.get("bias_soc"),
            "r2_soc": stats.get("r2_soc"),
            "rmse_flux": stats.get("rmse_flux"),
            "rmse_yield": stats.get("rmse_yield"),
        },
        "notes": [
            "本レポートは簡易 MRV モジュールに基づく試算です。",
            "実プロジェクトではサンプリング設計・不確実性評価・リーケージ等の精緻化が必要です。",
        ],
    }

    report["n_points"] = int(min(len(model_df), len(obs_df)))
    return report
