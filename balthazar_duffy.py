import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp


def concentration_decay(time, concentration, rate_constant):
    return -rate_constant * concentration


def main():
    rate_constant = 0.4  # min^-1
    initial_concentration = 1.0  # mol/L
    time_span = (0.0, 10.0)  # min
    evaluation_times = np.linspace(*time_span, 200)

    solution = solve_ivp(
        concentration_decay,
        time_span,
        [initial_concentration],
        args=(rate_constant,),
        t_eval=evaluation_times,
    )

    if not solution.success:
        raise RuntimeError(solution.message)

    plt.plot(solution.t, solution.y[0], label="Numerical solution")
    plt.xlabel("Time (min)")
    plt.ylabel("Concentration (mol/L)")
    plt.title("First-order concentration decay")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()