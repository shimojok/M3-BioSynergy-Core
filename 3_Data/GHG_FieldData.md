# GHG_FieldData — Data Specification

## 1. Data Dictionary

| Column | Meaning | Units | Notes |
|--------|---------|--------|-------|
| Day | Measurement day | days | Time index |
| CH4_ppm | Methane concentration | ppm | Used in CH₄ flux model |
| CO2_ppm | Carbon dioxide | ppm | Used in CO₂ exchange model |
| N2O_ppm | Nitrous oxide | ppm | Used in nitrogen flux model |
| Temperature | Soil temperature | °C | Affects reaction rates |
| Moisture | Soil water content | % | Feedback variable |

---

## 2. Model Integration

- **CH4_ppm** → methane flux model（F_CH4）
- **CO2_ppm** → CO₂ exchange model（F_CO2）
- **N2O_ppm** → nitrogen flux model（F_N2O）
- **Temperature** → modifies enzyme Vmax and microbial growth rate
- **Moisture** → modifies microbial growth and soil–atmosphere exchange

---

## 3. Usage

- Calibration of greenhouse gas reduction models  
- MRV（Monitoring, Reporting, Verification）  
- Climate finance quantification（carbon credits）  
- Validation of hypercycle simulation outputs  
