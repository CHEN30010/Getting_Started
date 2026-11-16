"""Integrate dy/dt = -2y with RK4 and display the solution."""

import matplotlib.pyplot as plt


def derivative(t, y):
    return -2 * y


t_start, t_end = 0.0, 5.0
dt = 0.01
steps = round((t_end - t_start) / dt)

times = [t_start]
values = [1.0]

for _ in range(steps):
    t = times[-1]
    y = values[-1]

    k1 = derivative(t, y)
    k2 = derivative(t + dt / 2, y + dt * k1 / 2)
    k3 = derivative(t + dt / 2, y + dt * k2 / 2)
    k4 = derivative(t + dt, y + dt * k3)

    values.append(y + dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6)
    times.append(t + dt)

plt.plot(times, values, label="Numerical solution")
plt.xlabel("Time (t)")
plt.ylabel("y(t)")
plt.title("Solution of dy/dt = -2y")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
