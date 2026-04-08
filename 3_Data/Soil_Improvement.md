# Soil_Improvement — Data Specification

## 1. Data Dictionary

| Column      | Meaning                     | Units | Notes                                      |
|-------------|------------------------------|--------|--------------------------------------------|
| Day         | Measurement day              | days   | Time index                                 |
| Organic_C   | Soil organic carbon          | %      | Used in carbon pool model (C_s)            |
| Total_N     | Total nitrogen               | %      | Used in nitrogen pool model (N_s)          |
| CN_Ratio    | Carbon–nitrogen ratio        | –      | Indicator of soil fertility                 |
| pH          | Soil acidity                 | –      | Affects enzyme kinetics and microbial growth |
| Moisture    | Soil water content           | %      | Links to Gaia moisture feedback (W)        |

---

## 2. Model Integration

- **Organic_C** → initializes and updates **soil carbon pool (C_s)**  
- **Total_N** → initializes and updates **soil nitrogen pool (N_s)**  
- **CN_Ratio** → influences microbial growth efficiency and enzyme cascade throughput  
- **pH** → modifies enzyme Vmax and microbial growth rate  
- **Moisture** → feeds into Earth System Ecology model (soil–atmosphere exchange, drought resilience)

This dataset is used to calibrate:
- Carbon flux acceleration model  
- Nitrogen flux model  
- Soil–atmosphere exchange model  
- Gaia feedback coupling (temperature & moisture)

---

## 3. Usage

- Soil regeneration monitoring  
- Calibration of hypercycle simulation parameters  
- MRV (Monitoring, Reporting, Verification) for carbon credits  
- Field validation of MBT55 deployment  
- Government and corporate reporting for soil health programs  
