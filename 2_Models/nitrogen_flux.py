"""
Nitrogen Flux Model
"""

def nitrogen_flux(N, beta):
    return beta * N

def update_nitrogen(N, beta, dt=0.1):
    return N + nitrogen_flux(N, beta) * dt
