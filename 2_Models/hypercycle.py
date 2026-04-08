"""
Hypercycle Integration Model
Combines microbial, enzyme, and flux models
"""

from microbial_dynamics import update_population
from enzyme_cascade import run_cascade
from carbon_flux import update_carbon
from nitrogen_flux import update_nitrogen

def hypercycle_step(N, S, C, N2):
    N = update_population(N, r=0.4, K=1.0)
    S = run_cascade(S, [0.2, 0.1])
    C = update_carbon(C, alpha=0.3)
    N2 = update_nitrogen(N2, beta=0.25)
    return N, S, C, N2
