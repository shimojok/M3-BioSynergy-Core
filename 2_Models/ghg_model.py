"""
GHG Reduction Model
"""

def ghg_reduction(CH4, CO2, rate):
    CH4_new = CH4 * (1 - rate)
    CO2_new = CO2 * (1 - rate * 0.5)
    return CH4_new, CO2_new
