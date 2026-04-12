import pandas as pd
from typing import Dict, Any


def _series_to_list(df: pd.DataFrame, col: str):
    return df[col].tolist() if col in df.columns else []


def export_soil_module_state(
    baseline_df: pd.DataFrame,
    project_df: pd.DataFrame,
    params: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Planetary OS Soil Module 形式の JSON を生成する。

    baseline_df / project_df:
        - year
        - soc_tC_ha
        - sequestration_tco2e_ha_yr
        - yield_t_ha
        - microbial_biomass
        - substrate
        - soil_stability
        - soil_n_tN_ha
        - n_loss_tN_ha_yr
    """
    diff_df = project_df.copy()
    for col in [
        "soc_tC_ha",
        "sequestration_tco2e_ha_yr",
        "yield_t_ha",
        "microbial_biomass",
        "soil_n_tN_ha",
        "n_loss_tN_ha_yr",
    ]:
        if col in project_df.columns and col in baseline_df.columns:
            diff_df[col] = project_df[col] - baseline_df[col]

    export = {
        "module": "soil",
        "version": "1.0",
        "area_ha": float(params.get("area_ha", 0.0)),
        "years": int(params.get("years", len(baseline_df))),
        "initial_soc_tC_ha": float(params.get("initial_soc", 0.0)),
        "scenario": {
            "mbt_dose_baseline": 0.0,
            "mbt_dose_project": float(params.get("mbt_dose", 0.0)),
        },
        "baseline": {
            "year": _series_to_list(baseline_df, "year"),
            "soc_tC_ha": _series_to_list(baseline_df, "soc_tC_ha"),
            "sequestration_tco2e_ha_yr": _series_to_list(
                baseline_df, "sequestration_tco2e_ha_yr"
            ),
            "yield_t_ha": _series_to_list(baseline_df, "yield_t_ha"),
        },
        "project": {
            "year": _series_to_list(project_df, "year"),
            "soc_tC_ha": _series_to_list(project_df, "soc_tC_ha"),
            "sequestration_tco2e_ha_yr": _series_to_list(
                project_df, "sequestration_tco2e_ha_yr"
            ),
            "yield_t_ha": _series_to_list(project_df, "yield_t_ha"),
        },
        "difference": {
            "soc_tC_ha": _series_to_list(diff_df, "soc_tC_ha"),
            "sequestration_tco2e_ha_yr": _series_to_list(
                diff_df, "sequestration_tco2e_ha_yr"
            ),
            "yield_t_ha": _series_to_list(diff_df, "yield_t_ha"),
        },
    }

    return export
