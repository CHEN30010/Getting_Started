"""Integrate a simple ODE (damped harmonic oscillator) and plot the result."""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt


def damped_oscillator(t, y, zeta=0.2, omega0=2.0):
    """y = [position, velocity]; y'' + 2*zeta*omega0*y' + omega0^2*y = 0."""
    x, v = y
    dxdt = v
    dvdt = -2 * zeta * omega0 * v - omega0**2 * x
    return [dxdt, dvdt]


def main():
    t_span = (0.0, 20.0)
    t_eval = np.linspace(*t_span, 500)
    y0 = [1.0, 0.0]  # initial position and velocity

    sol = solve_ivp(damped_oscillator, t_span, y0, t_eval=t_eval, method="RK45")

    plt.figure(figsize=(8, 5))
    plt.plot(sol.t, sol.y[0], label="position x(t)")
    plt.plot(sol.t, sol.y[1], label="velocity v(t)")
    plt.xlabel("time")
    plt.ylabel("value")
    plt.title("Damped Harmonic Oscillator")
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()
