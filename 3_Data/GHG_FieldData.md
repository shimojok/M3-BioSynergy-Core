# GHG_FieldData — Data Specification

## 1. Overview
Field measurements of greenhouse gases and soil conditions.

## 2. Data Dictionary

| Column | Meaning | Units | Notes |
|--------|---------|--------|-------|
| Day | Measurement day | days | Time index |
| CH4_ppm | Methane concentration | ppm | Used in CH₄ flux model |
| CO2_ppm | Carbon dioxide | ppm | Used in CO₂ exchange model |
| N2O_ppm | Nitrous oxide | ppm | Used in nitrogen flux model |
| Temperature | Soil temperature | °C | Affects reaction rates |
| Moisture | Soil water content | % | Feedback variable |

## 3. Model Integration

- CH₄ → F_CH4  
- CO₂ → F_CO2  
- N₂O → F_N2O  
- Temperature → modifies Vmax  
- Moisture → modifies microbial growth  

## 4. Usage
- Calibration of GHG reduction model  
- MRV (Monitoring, Reporting, Verification)  
- Climate finance quantification
