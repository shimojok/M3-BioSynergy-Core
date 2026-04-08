"""
Carbon Flux Acceleration Model
"""

def carbon_flux(C, alpha):
    return alpha * C

def update_carbon(C, alpha, dt=0.1):
    return C + carbon_flux(C, alpha) * dt
