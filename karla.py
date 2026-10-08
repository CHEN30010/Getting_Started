
# Solving the ODE dy/dt = -2y using Euler's method

t = 0
y = 10
dt = 0.1

for i in range(10):
    print("Time:", round(t, 2), "Solution:", round(y, 4))
    y = y - 2 * y * dt
    t = t + dt
