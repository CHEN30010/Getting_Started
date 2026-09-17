"""Simple ODE solver for a first-order equation y' = f(t, y).

This example solves the ODE
    y' = -2y
with initial condition y(0) = 1.
The exact solution is y(t) = exp(-2t).
"""

from __future__ import annotations

import math
from typing import Callable, List, Tuple

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def euler_method(
    f: Callable[[float, float], float],
    y0: float,
    t0: float,
    tf: float,
    h: float = 0.1,
) -> Tuple[List[float], List[float]]:
    """Approximate y' = f(t, y) using Euler's method."""
    if h <= 0:
        raise ValueError("Step size h must be positive.")

    t_values = [t0]
    y_values = [y0]
    t = t0
    y = y0

    while t < tf:
        y = y + h * f(t, y)
        t = t + h
        t_values.append(t)
        y_values.append(y)

    return t_values, y_values


def rk4_method(
    f: Callable[[float, float], float],
    y0: float,
    t0: float,
    tf: float,
    h: float = 0.1,
) -> Tuple[List[float], List[float]]:
    """Approximate y' = f(t, y) using the fourth-order Runge-Kutta method."""
    if h <= 0:
        raise ValueError("Step size h must be positive.")

    t_values = [t0]
    y_values = [y0]
    t = t0
    y = y0

    while t < tf:
        k1 = f(t, y)
        k2 = f(t + 0.5 * h, y + 0.5 * h * k1)
        k3 = f(t + 0.5 * h, y + 0.5 * h * k2)
        k4 = f(t + h, y + h * k3)

        y = y + (h / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        t = t + h

        t_values.append(t)
        y_values.append(y)

    return t_values, y_values


def exact_solution(t: float) -> float:
    """Exact solution for y' = -2y, y(0) = 1."""
    return math.exp(-2.0 * t)


def main() -> None:
    def f(t: float, y: float) -> float:
        return -2.0 * y

    t0 = 0.0
    tf = 1.0
    h = 0.1

    euler_t, euler_y = euler_method(f, y0=1.0, t0=t0, tf=tf, h=h)
    rk4_t, rk4_y = rk4_method(f, y0=1.0, t0=t0, tf=tf, h=h)

    print("t        Euler        RK4          Exact")
    for i in range(len(euler_t)):
        t = euler_t[i]
        e = euler_y[i]
        r = rk4_y[i]
        x = exact_solution(t)
        print(f"{t:4.1f}   {e:10.6f}   {r:10.6f}   {x:10.6f}")

    exact_t = [t for t in euler_t]
    exact_y = [exact_solution(t) for t in exact_t]

    plt.figure(figsize=(8, 5))
    plt.plot(euler_t, euler_y, label="Euler", marker="o", linestyle="--")
    plt.plot(rk4_t, rk4_y, label="RK4", marker="s", linestyle="-")
    plt.plot(exact_t, exact_y, label="Exact", color="black", linewidth=2)
    plt.xlabel("Time t")
    plt.ylabel("Response y(t)")
    plt.title("Simple ODE Solution: y' = -2y")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig("ode_response_vs_time.png", dpi=200)
    print("\nPlot saved to ode_response_vs_time.png")


if __name__ == "__main__":
    main()
