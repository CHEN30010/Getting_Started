import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Define the ODE: dy/dt = -0.2 * y
def model(t, y):
    return -0.2 * y

# Initial conditions and time span
y0 = [2.0]             # Initial value of y at t = 0
t_span = (0, 10)       # Start and end time
t_eval = np.linspace(0, 10, 100) # Points to evaluate the solution

# Run the solver
sol = solve_ivp(model, t_span, y0, t_eval=t_eval)

# Plot the results
plt.plot(sol.t, sol.y[0], label='y(t)')
plt.xlabel('Time t')
plt.ylabel('Y')
plt.title('ODE Simulation')
plt.legend()
plt.grid(True)
plt.show()
