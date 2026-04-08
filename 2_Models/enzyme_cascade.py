"""
Enzyme Cascade Model
Simulates multi-step enzymatic reactions
"""

import numpy as np

def cascade_step(S, k):
    """
    S : substrate concentration
    k : reaction rate
    """
    return -k * S

def run_cascade(S0, k_list, dt=0.1):
    S = S0
    for k in k_list:
        S += cascade_step(S, k) * dt
    return S

if __name__ == "__main__":
    S = run_cascade(1.0, [0.2, 0.1, 0.05])
    print("Final substrate:", S)
