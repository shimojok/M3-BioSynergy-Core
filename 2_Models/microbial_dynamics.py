"""
Microbial Dynamics Model
MBT55 population growth and interaction dynamics
"""

import numpy as np

def microbial_growth(N, r, K):
    """
    Logistic growth model
    N : population
    r : growth rate
    K : carrying capacity
    """
    return r * N * (1 - N / K)

def update_population(N, r, K, dt=0.1):
    return N + microbial_growth(N, r, K) * dt

if __name__ == "__main__":
    N = 0.1
    for t in range(50):
        N = update_population(N, r=0.5, K=1.0)
        print(t, N)
