# Thomas Butler - CHEN30010 Getting Started
# Solves a simple ODE: first-order reaction A -> B, dCA/dt = -k*CAi
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

k = 0.5      # rate constant (1/min)
CA0 = 1.0    # initial concentration (mol/L)

def rate(t, CA):
    return -k * CA

t_span = (0, 10)
t_eval = np.linspace(0, 10, 101)
sol = solve_ivp(rate, t_span, [CA0], t_eval=t_eval)

# Compare with analytical solution CA = CA0*exp(-k t)
analytical = CA0 * np.exp(-k * sol.t)
print(f"CA at t=10 min: numerical={sol.y[0][-1]:.5f}, analytical={analytical[-1]:.5f}")

plt.plot(sol.t, sol.y[0], label="solve_ivp")
plt.plot(sol.t, analytical, "--", label="analytical")
plt.xlabel("t (min)")
plt.ylabel("CA (mol/L)")
plt.legend()
plt.title("First-order reaction A -> B")
plt.show()