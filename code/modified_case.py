"""Related case: a Kenyan e-commerce site (peak sales day) rents three server types.
Minimise hourly cost while meeting BOTH a request-capacity and a memory requirement,
with a rack limit on the number of servers."""
import numpy as np
from scipy.optimize import minimize, linprog
from itertools import product

names = ["Type A (general)", "Type B (high-throughput)", "Type C (high-memory)"]
cost = np.array([12.0, 18.0, 30.0])     # USD per hour
cap  = np.array([100., 170., 120.])     # requests/second handled
mem  = np.array([ 64.,  32., 128.])     # GB RAM
REQ_CAP, REQ_MEM, MAX_SERVERS = 1500.0, 900.0, 20

obj = lambda z: cost @ z
cons = [
    {"type": "ineq", "fun": lambda z: cap @ z - REQ_CAP},
    {"type": "ineq", "fun": lambda z: mem @ z - REQ_MEM},
    {"type": "ineq", "fun": lambda z: MAX_SERVERS - z.sum()},
]
sol = minimize(obj, x0=[5, 5, 2], method="SLSQP", bounds=[(0, None)]*3, constraints=cons)
print("SLSQP success:", sol.success)
for n, v in zip(names, sol.x): print(f"{n}: {v:.3f}")
print(f"Capacity: {cap @ sol.x:.1f} req/s | Memory: {mem @ sol.x:.1f} GB | Servers: {sol.x.sum():.2f}")
print(f"Minimum hourly cost (continuous): {sol.fun:.2f}")

# Cross-check with linear programming
lp = linprog(cost, A_ub=[-cap, -mem, np.ones(3)], b_ub=[-REQ_CAP, -REQ_MEM, MAX_SERVERS], bounds=[(0, None)]*3)
print(f"linprog check: {lp.x.round(3)} cost={lp.fun:.2f}")

# Whole servers only
best = None
for a, b, c in product(range(MAX_SERVERS+1), repeat=3):
    if a+b+c <= MAX_SERVERS and cap @ [a,b,c] >= REQ_CAP and mem @ [a,b,c] >= REQ_MEM:
        tc = cost @ [a,b,c]
        if best is None or tc < best[0]: best = (tc, a, b, c)
tc, a, b, c = best
print(f"Best whole-server plan: A={a}, B={b}, C={c}, cost={tc:.2f}/h, "
      f"capacity={cap @ [a,b,c]:.0f} req/s, memory={mem @ [a,b,c]:.0f} GB")