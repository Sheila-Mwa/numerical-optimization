# Numerical Optimization
## 1. Mathematical concept
Optimization finds input values that minimize or maximize an objective function, usually subject to constraints. Here we minimize a linear cost function subject to a minimum-capacity inequality and non-negativity bounds, using scipy.optimize.minimize (method SLSQP)

## 2. Problem (code/optimization.py)
A cloud service chooses how many Type A and Type B servers to run

**Inputs**
|Item | Type A | Type B |
| --- | --- | --- |
| Cost per unit | 12 | 18 |
|Capacity per unit | 100 | 170 |

Required total capacity: at least 1000. Starting guess x0 = [5,3]. Bounds: x >= 0, y >=0.

**Mathematical operation** Minimize C(x,y) = 12*x + 18*y subject to 100*x + 170*y >= 1000, x >= 0, y >= 0.

**Output**
* Success: True
* Type A = 0.000, Type B = 5.882
* Total capacity = 1000.00
* Minimum planning cost = 105.88
* Best integer solution: Type B servers, cost 108, capacity 1020

### Explanation
Cost per unit of capacity is 12/100 = 0.120 for Type A and 18/170 = 0.106 for Type B. B is cheaper per unit capacity, so the optimizer uses only B and stops exactly when capacity reaches 1000. Since 5.882 server cannot be bought, the integer search shows that 6 Type B servers is the cheapest whole-server plan, this is slightly above the continuous optimum 105.88 because of rounding up

## 3. Changing the parameters(code/changed_parameters.py)

| Case | Continuous optimum | Integer optimum | What changed
| ------------ | ------------ | ----------- | ------------------- |
| Original | A=0, B=5.882, cost 105.88 | B=6, cost 108 | - |
| Required capacity 1000 → 1500 | A=0, B=8.824, cost 158.82 | B=9, cost 162 | Need rises 50%, cost rises about 50% (105.88 → 158.82) because the constraint is active and the model is linear. |
| Type B cost 18 → 25 | A=10, B=0, cost 120.00 | A=10, cost 120 | B now costs 25/170 ≈ 0.147 per capacity unit, worse than A's 0.120, so the optimizer switches entirely to A. |

Conclusion: the answer depends on the cost per capacity ration, not on the cost alone. A small price change can flip the whole allocation.

## 4. Modified real-world case (code/modified_case.py)
Scenario: an e-commerce website in Kenya expects a peak sales day (for example Black Friday). It rents three server types and must meet BOTH a request-handling requirement and a memory requirement, with a limit on rack space.

**New assumptions**
* Costs are per hour (USD), capacity is in requests/second, memory in GB.
* Servers are available in unlimited supply except for a maximum of 20 in total.
* Capacity and memory add up linearly across servers, no discounts.

**Input data**

| Server | Cost/hour | Capacity (req/s) | Memory (GB) |
| ---- | ---- | ---- | ---- |
| A (general) | 12 | 100 | 64 |
| B (high-throughput) | 18 | 170 | 32 |
| C (high-memory) | 30 | 120 | 128 |


Requirements: capacity >= 1500 req/s, memory >= 900 GB, total servers <= 20.

Model: minimize 12A + 18B + 30C subject to the three constraints and A, B, C >= 0.

**Output**
* SLSQP: A = 13.672, B = 0.781, C = 0, cost = 178.13/hour (capacity 1500, memory 900, 14.45 servers)
* linprog cross-check agrees: cost 178.12
* Best whole-server plan: A = 15, B = 0, C = 0, cost 180/hour, capacity 1500 req/s, memory 960 GB

**Interpretation**
Both the capacity and memory constraints are active in the continuous solution: the optimizer mixes A (which supplies memory cheaply) with a little B (cheap capacity). Type C is never chosen because its memory is more expensive than getting memory from A. When whole servers are required, 15 Type A servers is the cheapest valid plan at 180/hour, only 1.1% above the continuous lower bound of 178.13 and uses 15 of the 20 allowed servers. This shows how adding a second requirement changes the answer: the original problem chose only B, but the memory requirement now makes A necessary.

## 5. How to run
```
pip install numpy scipy
python code/optimization.py
python code/changed_parameters.py
python code/modified_case.py
```
