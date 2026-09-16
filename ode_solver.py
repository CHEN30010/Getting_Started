"""A small SciPy-based solver for first-order ordinary differential equations."""

from collections.abc import Callable, Sequence

import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp


State = list[float]
Derivative = Callable[[float, Sequence[float]], Sequence[float]]


def solve_ode(
    derivative: Derivative,
    t_span: tuple[float, float],
    initial_state: Sequence[float],
    step_size: float,
) -> tuple[list[float], list[State]]:
    """Solve y'(t) = derivative(t, y) with SciPy's adaptive RK45 method."""
    start, end = t_span
    if end <= start:
        raise ValueError("t_span must have an increasing start and end")
    if step_size <= 0:
        raise ValueError("step_size must be positive")
    if not initial_state:
        raise ValueError("initial_state must not be empty")

    result = solve_ivp(
        derivative,
        t_span,
        initial_state,
        max_step=step_size,
    )
    if not result.success:
        raise RuntimeError(result.message)

    return result.t.tolist(), result.y.T.tolist()


def plot_solution(times: Sequence[float], states: Sequence[Sequence[float]], output_path: str) -> None:
    """Plot each state variable and save the figure to output_path."""
    figure, axis = plt.subplots()
    state_count = len(states[0])
    for state_index in range(state_count):
        values = [state[state_index] for state in states]
        axis.plot(times, values, label=f"y{state_index + 1}")

    axis.set_xlabel("t")
    axis.set_ylabel("state")
    axis.set_title("ODE solution")
    axis.grid(True, alpha=0.3)
    if state_count > 1:
        axis.legend()
    figure.tight_layout()
    figure.savefig(output_path, dpi=150)
    plt.close(figure)


if __name__ == "__main__":
    # y' = -y, y(0) = 1; the exact solution is y(t) = exp(-t).
    times, states = solve_ode(
        lambda _time, state: [-state[0]],
        t_span=(0.0, 1.0),
        initial_state=[1.0],
        step_size=0.1,
    )
    print(f"y(0) = {states[0][0]:.4f}")
    print(f"y(1) ~= {states[-1][0]:.4f}")
    plot_solution(times, states, "ode_solution.png")
    print("Plot saved to ode_solution.png")
