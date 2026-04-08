# MBT55_Composition — Data Specification

## 1. Overview
This dataset defines the microbial composition of the MBT55 consortium used in the Planetary OS hypercycle model.

## 2. Data Dictionary

| Column | Meaning | Units | Notes |
|--------|---------|--------|-------|
| Microbe | Taxonomic group | – | Functional group in MBT55 |
| Relative_Abundance | Fraction of total biomass | 0–1 | Used in microbial dynamics model |
| Function | Ecological role | – | Links to enzyme cascade |

## 3. Model Integration

### 3.1 Microbial Dynamics Model
- Relative_Abundance initializes **N (microbial biomass)**  
- Determines growth rate modifiers  
- Influences carrying capacity K

### 3.2 Enzyme Cascade Model
- Microbial groups map to enzyme production rates  
- Oxidizers → oxidoreductase  
- Decomposers → hydrolase  
- Fermenters → transferase precursors

### 3.3 Nitrogenase Model
- Nitrogen-transforming microbes influence **E_nit (nitrogenase concentration)**

## 4. Usage
- Load in Python using pandas  
- Connect to hypercycle simulation  
- Use for calibration and field validation
