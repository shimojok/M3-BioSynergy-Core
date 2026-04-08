# HeavyMetal_Transformation — Data Specification

## 1. Data Dictionary

| Column                | Meaning                       | Units | Notes                                      |
|-----------------------|-------------------------------|--------|--------------------------------------------|
| Metal                 | Heavy metal type              | –      | Cd, Pb, As, Cr, etc.                       |
| Initial_mg_per_kg     | Initial concentration         | mg/kg  | Baseline contamination level               |
| After_30d_mg_per_kg   | Final concentration           | mg/kg  | Post-MBT55 treatment                       |
| Reduction_Rate        | Fraction removed              | 0–1    | Used in detoxification model               |
| Mechanism             | Biological transformation path| –      | Links to nitrogenase & enzyme cascade      |

---

## 2. Model Integration

- **Reduction_Rate** → defines detoxification coefficient in the nitrogenase model  
- **Mechanism** → maps to:
  - nitrogenase electron transfer pathways  
  - enzyme cascade (oxidoreductase, lyase)  
  - microbial redox cycling  

This dataset calibrates:
- Heavy metal transformation model  
- Soil toxicity reduction model  
- Claim Engine validation for pollution remediation credits  

---

## 3. Usage

- Environmental remediation reporting  
- Validation of MBT55’s pollutant reduction performance  
- MRV for heavy-metal reduction credits  
- Government compliance (soil quality standards)  
- Industrial wastewater treatment monitoring  
