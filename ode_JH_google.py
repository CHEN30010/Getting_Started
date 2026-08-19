import numpy as np
from scipy.integrate import odeint, solve_ivp
import matplotlib.pyplot as plt

# Example 1: Simple unimolecular reaction A → B
# Rate equation: dA/dt = -k*A, dB/dt = k*A

def reaction_simple(y, t, k):
    """
    Simple first-order reaction: A → B
    y[0] = concentration of A
    y[1] = concentration of B
    k = rate constant
    """
    A, B = y
    dAdt = -k * A
    dBdt = k * A
    return [dAdt, dBdt]

# Example 2: Bimolecular reaction A + B → C
# Rate equation: dA/dt = -k*A*B, dB/dt = -k*A*B, dC/dt = k*A*B

def reaction_bimolecular(y, t, k):
    """
    Bimolecular reaction: A + B → C
    y[0] = concentration of A
    y[1] = concentration of B
    y[2] = concentration of C
    k = rate constant
    """
    A, B, C = y
    dAdt = -k * A * B
    dBdt = -k * A * B
    dCdt = k * A * B
    return [dAdt, dBdt, dCdt]

# Example 3: Consecutive reaction A → B → C
# Rate equations: dA/dt = -k1*A, dB/dt = k1*A - k2*B, dC/dt = k2*B

def reaction_consecutive(y, t, k1, k2):
    """
    Consecutive reaction: A → B → C
    y[0] = concentration of A
    y[1] = concentration of B
    y[2] = concentration of C
    k1, k2 = rate constants
    """
    A, B, C = y
    dAdt = -k1 * A
    dBdt = k1 * A - k2 * B
    dCdt = k2 * B
    return [dAdt, dBdt, dCdt]

# ============= Solving the ODEs =============

# Time span
t = np.linspace(0, 10, 1000)

# Initial concentrations
y0_simple = [1.0, 0.0]          # [A]₀, [B]₀
y0_bimolecular = [1.0, 1.0, 0.0] # [A]₀, [B]₀, [C]₀
y0_consecutive = [1.0, 0.0, 0.0] # [A]₀, [B]₀, [C]₀

# Rate constants
k = 0.5      # for simple and bimolecular
k1, k2 = 0.5, 0.3  # for consecutive

# Solve ODEs using odeint
print("Solving chemical reaction ODEs...\n")

solution_simple = odeint(reaction_simple, y0_simple, t, args=(k,))
solution_bimolecular = odeint(reaction_bimolecular, y0_bimolecular, t, args=(k,))
solution_consecutive = odeint(reaction_consecutive, y0_consecutive, t, args=(k1, k2))

print(f"Simple reaction at t=10: A={solution_simple[-1, 0]:.4f}, B={solution_simple[-1, 1]:.4f}")
print(f"Bimolecular reaction at t=10: A={solution_bimolecular[-1, 0]:.4f}, B={solution_bimolecular[-1, 1]:.4f}, C={solution_bimolecular[-1, 2]:.4f}")
print(f"Consecutive reaction at t=10: A={solution_consecutive[-1, 0]:.4f}, B={solution_consecutive[-1, 1]:.4f}, C={solution_consecutive[-1, 2]:.4f}\n")

# ============= Plotting Results =============

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# Plot 1: Simple reaction
axes[0].plot(t, solution_simple[:, 0], 'b-', label='[A]', linewidth=2)
axes[0].plot(t, solution_simple[:, 1], 'r-', label='[B]', linewidth=2)
axes[0].set_xlabel('Time (s)', fontsize=10)
axes[0].set_ylabel('Concentration (M)', fontsize=10)
axes[0].set_title('Simple Reaction: A → B', fontsize=12, fontweight='bold')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Plot 2: Bimolecular reaction
axes[1].plot(t, solution_bimolecular[:, 0], 'b-', label='[A]', linewidth=2)
axes[1].plot(t, solution_bimolecular[:, 1], 'g-', label='[B]', linewidth=2)
axes[1].plot(t, solution_bimolecular[:, 2], 'r-', label='[C]', linewidth=2)
axes[1].set_xlabel('Time (s)', fontsize=10)
axes[1].set_ylabel('Concentration (M)', fontsize=10)
axes[1].set_title('Bimolecular Reaction: A + B → C', fontsize=12, fontweight='bold')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

# Plot 3: Consecutive reaction
axes[2].plot(t, solution_consecutive[:, 0], 'b-', label='[A]', linewidth=2)
axes[2].plot(t, solution_consecutive[:, 1], 'g-', label='[B]', linewidth=2)
axes[2].plot(t, solution_consecutive[:, 2], 'r-', label='[C]', linewidth=2)
axes[2].set_xlabel('Time (s)', fontsize=10)
axes[2].set_ylabel('Concentration (M)', fontsize=10)
axes[2].set_title('Consecutive Reaction: A → B → C', fontsize=12, fontweight='bold')
axes[2].legend()
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()