import numpy as np
from scipy.optimize import minimize

def solve(cost_a, cost_b, cap_a, cap_b, required, label):
    cost = lambda z: cost_a*z[0] + cost_b*z[1]
    cons = {"type": "ineq", "fun": lambda z: cap_a*z[0] + cap_b*z[1] - required}
    s = minimize(cost, x0=[5, 3], method="SLSQP", bounds=[(0, None)]*2, constraints=cons)
    best = None
    for a in range(0, 40):
        for b in range(0, 40):
            if cap_a*a + cap_b*b >= required:
                c = cost_a*a + cost_b*b
                if best is None or c < best[0]:
                    best = (c, a, b, cap_a*a + cap_b*b)
    print(f"--- {label} ---")
    print(f"Continuous: A={s.x[0]:.3f}, B={s.x[1]:.3f}, cost={s.fun:.2f}")
    print(f"Integer (cost, A, B, capacity): {best}\n")

solve(12, 18, 100, 170, 1000, "Original")
solve(12, 18, 100, 170, 1500, "Change 1: required capacity 1000 -> 1500")
solve(12, 25, 100, 170, 1000, "Change 2: Type B cost 18 -> 25")