"""Integrate and plot a simple damped harmonic oscillator."""

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp


def oscillator(t: float, state: np.ndarray) -> list[float]:
    """Return derivatives for x'' + 0.2 x' + x = 0."""
    position, velocity = state
    return [velocity, -0.2 * velocity - position]


def main() -> None:
    time_span = (0.0, 20.0)
    initial_state = [1.0, 0.0]
    times = np.linspace(*time_span, 1_000)

    solution = solve_ivp(
        oscillator,
        time_span,
        initial_state,
        t_eval=times,
        rtol=1e-8,
        atol=1e-10,
    )

    if not solution.success:
        raise RuntimeError(solution.message)

    plt.plot(solution.t, solution.y[0], label="position x(t)")
    plt.plot(solution.t, solution.y[1], label="velocity x'(t)")
    plt.xlabel("Time")
    plt.ylabel("State")
    plt.title("Damped harmonic oscillator")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()