
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# ============================================================
# CHEN30010 TEAM 12 - AE630 FED-BATCH REACTOR
# Dynamic energy balance and cooling failure investigation
# PRELIMINARY EDUCATIONAL MODEL - NOT AN OPERATING PROCEDURE
# ============================================================

# -------------------------
# 1. REACTOR PARAMETERS
# -------------------------

n_A0 = 100.0               # mol
V_initial = 400.0          # L
V_feed = 100.0             # L

agitator_rpm = 90
UA = 475.039               # W/K, Dynochem estimate at 400 L

density = 930.0            # kg/m3, approximate
Cp = 1900.0                # J/(kg K), approximate

T_initial = 25.0           # Celsius
T_feed = 25.0              # Celsius, assumed
T_jacket = 20.0            # Celsius
T_max = 35.0               # Celsius

# -------------------------
# 2. SODIUM ETHOXIDE FEED
# -------------------------

NaOEt_concentration = 1.0  # mol/L, trial value
feed_time = 150.0          # min, trial value

feed_flow = V_feed / feed_time
NaOEt_total = NaOEt_concentration * V_feed

# Cooling fails after half the feed is added
failure_time = feed_time / 2.0

# -------------------------
# 3. REACTION KINETICS
# -------------------------

k1_ref = 161.3             # L/(mol min)
k2_ref = 1.164             # 1/min
k3_ref = 0.0027            # L/(mol min)

Ea1 = 26600.0              # J/mol
Ea2 = 87000.0
Ea3 = 81900.0

R = 8.314                  # J/(mol K)
T_ref = 298.15             # K

Keq = 10.0

# Reaction enthalpies (J/mol)
dH1 = -45000.0
dH2 = -120000.0
dH3 = -80000.0

# -------------------------
# 4. ETHANOL SOLVENT
# -------------------------

ethanol_density = 0.785    # kg/L
ethanol_MW = 46.07         # g/mol

ethanol_fraction = 0.40

n_EtOH0 = (
    ethanol_fraction
    * V_initial
    * ethanol_density
    * 1000.0
    / ethanol_MW
)

ethanol_feed_concentration = (
    ethanol_fraction
    * ethanol_density
    * 1000.0
    / ethanol_MW
)

# IMPORTANT:
# The reverse-rate expression below is a provisional
# concentration-based interpretation of Keq.
# It must be verified before quantitative design use.

def arrhenius(k_ref, Ea, T_C):
    T_K = T_C + 273.15
    return k_ref * np.exp(
        -(Ea / R) * (1.0 / T_K - 1.0 / T_ref)
    )


# -------------------------
# 5. DIFFERENTIAL EQUATIONS
# -------------------------

def reactor_model(t, y, cooling_active):

    A, A_salt, B, C, NaOEt, EtOH, T = y

    feeding = t < feed_time

    F = feed_flow if feeding else 0.0

    V = V_initial + feed_flow * min(t, feed_time)

    c_A = A / V
    c_salt = A_salt / V
    c_B = B / V
    c_NaOEt = NaOEt / V
    c_EtOH = EtOH / V

    k1 = arrhenius(k1_ref, Ea1, T)
    k2 = arrhenius(k2_ref, Ea2, T)
    k3 = arrhenius(k3_ref, Ea3, T)

    # Reaction rates in mol/(L min)
    r1_forward = k1 * c_A * c_NaOEt

    # Provisional reverse-rate expression
    k1_reverse = k1 / Keq
    r1_reverse = k1_reverse * c_salt * c_EtOH

    r1_net = r1_forward - r1_reverse
    r2 = k2 * c_salt
    r3 = k3 * c_B * c_NaOEt

    # Material balances, mol/min
    dA = -r1_net * V
    dSalt = (r1_net - r2) * V
    dB = (r2 - r3) * V
    dC = r3 * V

    dNaOEt = NaOEt_concentration * F - (
        r1_net + r3
    ) * V

    dEtOH = ethanol_feed_concentration * F + r1_net * V

    # -------------------------
    # ENERGY BALANCE
    # -------------------------

    # Reaction heat generation, J/min
    Q_reaction = -V * (
        dH1 * r1_net
        + dH2 * r2
        + dH3 * r3
    )

    # Jacket heat transfer, J/min
    if cooling_active:
        Q_jacket = UA * (T_jacket - T) * 60.0
    else:
        Q_jacket = 0.0

    # Incoming feed sensible heat, J/min
    feed_mass_rate = F * density / 1000.0

    Q_feed = feed_mass_rate * Cp * (T_feed - T)

    # Reactor heat capacity, J/K
    reactor_mass = V * density / 1000.0
    heat_capacity = reactor_mass * Cp

    dT = (
        Q_reaction + Q_jacket + Q_feed
    ) / heat_capacity

    return [
        dA, dSalt, dB, dC,
        dNaOEt, dEtOH, dT
    ]


# -------------------------
# 6. RUN A SCENARIO
# -------------------------

simulation_time = 1500.0

y0 = [
    n_A0,
    0.0,
    0.0,
    0.0,
    0.0,
    n_EtOH0,
    T_initial
]


def integrate_section(start, end, state, cooling):

    sol = solve_ivp(
        lambda t, y: reactor_model(t, y, cooling),
        (start, end),
        state,
        method="BDF",
        dense_output=True,
        rtol=1e-7,
        atol=1e-9,
        max_step=0.5
    )

    if not sol.success:
        raise RuntimeError(sol.message)

    return sol


def run_scenario(cooling_failure=False):

    if cooling_failure:
        sections = [
            (0.0, failure_time, True),
            (failure_time, feed_time, False),
            (feed_time, simulation_time, False)
        ]
    else:
        sections = [
            (0.0, feed_time, True),
            (feed_time, simulation_time, True)
        ]

    solutions = []
    state = np.array(y0, dtype=float)

    for start, end, cooling in sections:

        sol = integrate_section(start, end, state, cooling)

        solutions.append(sol)
        state = sol.y[:, -1]

    # Sample the piecewise solutions on a common time grid
    times = np.linspace(0, simulation_time, 3001)

    amounts = np.zeros((7, len(times)))

    for i, t in enumerate(times):

        for j, sol in enumerate(solutions):

            is_last = j == len(solutions) - 1

            if sol.t[0] <= t < sol.t[-1] or (
                is_last and t <= sol.t[-1]
            ):
                amounts[:, i] = sol.sol(t)
                break

    return times, amounts


normal_time, normal = run_scenario(False)
failure_time_grid, failure = run_scenario(True)


# -------------------------
# 7. IPC AND 60-MIN HOLD
# -------------------------

IPC_target = 0.01 * n_A0
hold_duration = 60.0
impurity_limit = 1.75


def interpolate_state(times, results, t):
    return np.array([
        np.interp(t, times, results[i])
        for i in range(results.shape[0])
    ])


def analyse_scenario(name, times, results):

    A = results[0]
    B = results[2]
    C = results[3]
    T = results[6]

    max_temp = np.max(T)
    max_temp_time = times[np.argmax(T)]

    print("\n" + "=" * 55)
    print(name)
    print("=" * 55)

    print(f"Maximum temperature: {max_temp:.3f} C")
    print(f"Time of maximum: {max_temp_time:.2f} min")

    print(
        "Temperature requirement:",
        "PASS" if max_temp <= T_max else "FAIL"
    )

    crossings = np.where(
        (A[:-1] > IPC_target)
        & (A[1:] <= IPC_target)
    )[0]

    if len(crossings) == 0:
        print("IPC NOT REACHED during simulation.")
        return None

    idx = crossings[0]

    # Linear interpolation for IPC crossing
    t1, t2 = times[idx], times[idx + 1]
    A1, A2 = A[idx], A[idx + 1]

    ipc_time = t1 + (
        (IPC_target - A1) * (t2 - t1) / (A2 - A1)
    )

    hold_end = ipc_time + hold_duration

    print(f"IPC crossing: {ipc_time:.2f} min")

    if hold_end > times[-1]:
        print("60-minute hold extends beyond simulation.")
        return ipc_time

    state_hold = interpolate_state(
        times, results, hold_end
    )

    A_hold = state_hold[0]
    B_hold = state_hold[2]
    C_hold = state_hold[3]
    T_hold = state_hold[6]

    impurity_percent = (
        100.0 * C_hold / B_hold
        if B_hold > 0 else float("nan")
    )

    print(f"End of hold: {hold_end:.2f} min")
    print(f"A after hold: {A_hold:.4f} mol")
    print(f"B after hold: {B_hold:.4f} mol")
    print(f"C after hold: {C_hold:.4f} mol")
    print(f"Temperature after hold: {T_hold:.3f} C")
    print(f"C/B after hold: {impurity_percent:.4f}%")

    print(
        "Impurity requirement:",
        "PASS" if impurity_percent < impurity_limit
        else "FAIL"
    )

    return ipc_time


normal_ipc = analyse_scenario(
    "NORMAL COOLING",
    normal_time,
    normal
)

failure_ipc = analyse_scenario(
    "COOLING FAILURE AT HALF FEED",
    failure_time_grid,
    failure
)


# -------------------------
# 8. TEMPERATURE COMPARISON
# -------------------------

plt.figure(figsize=(11, 6))

plt.plot(
    normal_time,
    normal[6],
    label="Normal cooling",
    linewidth=2
)

plt.plot(
    failure_time_grid,
    failure[6],
    label="Cooling failure",
    linewidth=2
)

plt.axhline(
    T_max,
    color="red",
    linestyle="--",
    label="35 C temperature limit"
)

plt.axvline(
    failure_time,
    color="grey",
    linestyle=":",
    label="Cooling failure at half feed"
)

plt.xlabel("Time (min)")
plt.ylabel("Reactor temperature (C)")
plt.title("AE630 - Normal Cooling vs Cooling Failure")

plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig(
    "cooling_failure_temperature.png",
    dpi=300
)


# -------------------------
# 9. INTERMEDIATE A
# -------------------------

plt.figure(figsize=(11, 6))

plt.plot(
    normal_time,
    normal[0],
    label="Normal cooling"
)

plt.plot(
    failure_time_grid,
    failure[0],
    label="Cooling failure"
)

plt.axhline(
    IPC_target,
    color="red",
    linestyle="--",
    label="1% IPC limit"
)

plt.axvline(
    feed_time,
    color="grey",
    linestyle=":",
    label="End of feed"
)

plt.xlabel("Time (min)")
plt.ylabel("Intermediate A (mol)")
plt.title("AE630 - Effect of Cooling Failure on A")

plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig(
    "cooling_failure_A.png",
    dpi=300
)


# -------------------------
# 10. IMPURITY COMPARISON
# -------------------------

plt.figure(figsize=(11, 6))

normal_ratio = np.divide(
    100.0 * normal[3],
    normal[2],
    out=np.full_like(normal[2], np.nan),
    where=normal[2] > 1e-9
)

failure_ratio = np.divide(
    100.0 * failure[3],
    failure[2],
    out=np.full_like(failure[2], np.nan),
    where=failure[2] > 1e-9
)

plt.plot(
    normal_time,
    normal_ratio,
    label="Normal cooling"
)

plt.plot(
    failure_time_grid,
    failure_ratio,
    label="Cooling failure"
)

plt.axhline(
    impurity_limit,
    color="red",
    linestyle="--",
    label="1.75% impurity limit"
)

plt.xlabel("Time (min)")
plt.ylabel("Impurity C/B (mol %)")
plt.title("AE630 - Effect of Cooling Failure on Impurity")

plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig(
    "cooling_failure_impurity.png",
    dpi=300
)

print("\nSaved three comparison graphs.")

print("\nIMPORTANT MODEL LIMITATIONS")
print("---------------------------")
print("Constant UA and approximate solvent properties.")
print("Adiabatic assumption after cooling failure.")
print("Reverse reaction equilibrium needs validation.")
print("No vessel heat losses after cooling failure.")
print("No detailed jacket or feed mixing dynamics.")
print("Results are preliminary and not safety validated.")

plt.show()

