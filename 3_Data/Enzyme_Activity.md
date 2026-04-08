# Enzyme_Activity — Data Specification

## 1. Data Dictionary

| Column              | Meaning                     | Units | Notes                                      |
|---------------------|------------------------------|--------|--------------------------------------------|
| Enzyme              | Enzyme class                | –      | Matches enzyme cascade model               |
| Activity_U_per_mL   | Enzyme activity             | U/mL   | Used to estimate Vmax in kinetic model     |
| Role                | Biochemical function        | –      | Links to reaction pathways                 |

---

## 2. Model Integration

- **Activity_U_per_mL** → directly maps to **Vmax** in the enzyme cascade model  
- **Enzyme** → determines which step of the cascade the activity influences  
  - Oxidoreductase → electron transfer  
  - Hydrolase → polymer breakdown  
  - Transferase → functional group transfer  
  - Lyase → bond cleavage  
- **Role** → used to classify reaction pathways in the hypercycle simulation

This dataset calibrates:
- Multi-step Michaelis–Menten kinetics  
- Substrate turnover rates  
- Carbon flux acceleration  
- Nitrogenase-linked redox pathways  

---

## 3. Usage

- Calibration of enzyme cascade parameters  
- Field validation of enzyme activity changes  
- Linking biochemical activity to carbon/nitrogen flux  
- MRV (Monitoring, Reporting, Verification) for climate finance  
- Scientific reproducibility for Planetary OS models  
