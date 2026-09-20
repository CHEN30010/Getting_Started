"""Integrate and plot the simple ODE dy/dt = -y, y(0) = 1."""

import math

import matplotlib.pyplot as plt


def derivative(time: float, value: float) -> float:
    """Return dy/dt for dy/dt = -y."""
    return -value


def rk4_step(time: float, value: float, step_size: float) -> float:
    """Advance one step using the classical fourth-order Runge-Kutta method."""
    slope_1 = derivative(time, value)
    slope_2 = derivative(time + step_size / 2, value + step_size * slope_1 / 2)
    slope_3 = derivative(time + step_size / 2, value + step_size * slope_2 / 2)
    slope_4 = derivative(time + step_size, value + step_size * slope_3)

    return value + step_size * (slope_1 + 2 * slope_2 + 2 * slope_3 + slope_4) / 6


def integrate_ode(
    initial_time: float,
    final_time: float,
    initial_value: float,
    step_size: float,
) -> tuple[list[float], list[float]]:
    """Integrate the ODE from initial_time to final_time."""
    times = [initial_time]
    values = [initial_value]

    while times[-1] < final_time:
        current_time = times[-1]
        current_step = min(step_size, final_time - current_time)
        next_value = rk4_step(current_time, values[-1], current_step)
        times.append(current_time + current_step)
        values.append(next_value)

    return times, values


def main() -> None:
    initial_time = 0.0
    final_time = 5.0
    initial_value = 1.0
    step_size = 0.1

    times, numerical_values = integrate_ode(
        initial_time, final_time, initial_value, step_size
    )
    exact_values = [initial_value * math.exp(-time) for time in times]
    final_error = abs(numerical_values[-1] - exact_values[-1])

    print(f"Numerical y({final_time:g}) = {numerical_values[-1]:.8f}")
    print(f"Exact y({final_time:g})     = {exact_values[-1]:.8f}")
    print(f"Absolute error          = {final_error:.3e}")

    plt.plot(times, numerical_values, "o", markevery=5, label="RK4 solution")
    plt.plot(times, exact_values, "-", label="Exact solution")
    plt.xlabel("Time, t")
    plt.ylabel("Solution, y(t)")
    plt.title(r"ODE solution: $dy/dt=-y$, $y(0)=1$")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()