"""
Unified Demo Script for M3-BioSynergy Core
"""

from hypercycle import hypercycle_step

def run_demo(steps=20):
    N, S, C, N2 = 0.1, 1.0, 0.5, 0.3
    for t in range(steps):
        N, S, C, N2 = hypercycle_step(N, S, C, N2)
        print(f"t={t}  Microbes={N:.3f}  Substrate={S:.3f}  C={C:.3f}  N={N2:.3f}")

if __name__ == "__main__":
    run_demo()
