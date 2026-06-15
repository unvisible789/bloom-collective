#!/usr/bin/env python3
"""
PMSM Validation Model - Baseline for Simulation Accuracy Testing
================================================================

Purpose:
This model simulates a surface-mount Permanent Magnet Synchronous Motor (PMSM)
using lumped parameters. It is intended to be validated against real bench test
data from verified electric motors.

Goal:
Establish confidence in the modeling approach (torque production, losses,
efficiency) before applying similar methods to experimental motor concepts.

How to Use for Validation:
1. Replace default parameters with values from a real motor datasheet or test report.
2. Compare simulation outputs (torque, efficiency, losses) against measured data.
3. Adjust model fidelity as needed (add iron loss modeling, temperature effects, etc.).

This is a validation reference, not a performance predictor for untested designs.

Typical Data Sources:
- Manufacturer datasheets (torque constant Kt, resistance, inductance)
- Research papers with dynamometer test results
- Open motor datasets (university labs, IEEE papers)

Author: Grok (xAI) + Daniel Brown collaboration
Date: 2026-06-15
"""

import numpy as np

print("=" * 80)
print("PMSM VALIDATION MODEL")
print("Baseline for comparing simulation accuracy against real tested motors")
print("=" * 80)

# ==================== MOTOR PARAMETERS ====================
# These should be replaced with real motor data for validation

# Electrical
R_s = 0.85               # Stator resistance per phase (Ω)
L_d = 0.012              # d-axis inductance (H)
L_q = 0.012              # q-axis inductance (H) - surface mount PMSM
psi_f = 0.085            # Permanent magnet flux linkage (Wb)

# Mechanical
pole_pairs = 4
J = 0.008                # Rotor inertia (kg.m²)
B = 0.001                # Viscous friction coefficient

# Operating point for validation
I_q = 12.0               # q-axis current (A) - torque producing
I_d = 0.0                # d-axis current (A) - usually 0 for surface mount
omega_mech = 1500 * 2 * np.pi / 60   # Mechanical speed (rad/s) ≈ 1500 RPM

# Loss factors (adjust based on real motor data)
copper_loss_factor = 1.0
iron_loss_factor = 0.6
mechanical_loss_factor = 0.4

# ==================== CALCULATIONS ====================
omega_elec = omega_mech * pole_pairs

# Torque production (surface-mount PMSM)
torque = (3/2) * pole_pairs * (psi_f * I_q + (L_d - L_q) * I_d * I_q)

# Back-EMF (line-to-neutral RMS)
E_back_emf = omega_elec * psi_f / np.sqrt(2)

# Copper losses
total_current_rms = np.sqrt(I_d**2 + I_q**2) / np.sqrt(2)
copper_losses = 3 * R_s * total_current_rms**2

# Approximate iron + mechanical losses (very simplified)
iron_mech_losses = (iron_loss_factor + mechanical_loss_factor) * (omega_mech ** 2) * 0.001

# Total losses and input power
total_losses = copper_losses + iron_mech_losses
mechanical_output_power = torque * omega_mech
input_power = mechanical_output_power + total_losses

efficiency = (mechanical_output_power / input_power) * 100 if input_power > 0 else 0

# ==================== RESULTS ====================
print(f"\nMotor Parameters (replace with real data):")
print(f"  Stator Resistance: {R_s:.3f} Ω/phase")
print(f"  Flux Linkage: {psi_f:.4f} Wb")
print(f"  Pole Pairs: {pole_pairs}")

print(f"\nOperating Point:")
print(f"  Speed: {omega_mech * 60 / (2 * np.pi):.0f} RPM")
print(f"  I_q: {I_q:.1f} A")
print(f"  I_d: {I_d:.1f} A")

print(f"\n--- Performance ---")
print(f"  Electromagnetic Torque: {torque:.2f} Nm")
print(f"  Back-EMF (RMS): {E_back_emf:.1f} V")
print(f"  Mechanical Output Power: {mechanical_output_power:.1f} W")
print(f"  Input Power (est): {input_power:.1f} W")
print(f"  Efficiency: {efficiency:.1f} %")

print(f"\n--- Losses ---")
print(f"  Copper Losses: {copper_losses:.1f} W")
print(f"  Iron + Mechanical Losses (approx): {iron_mech_losses:.1f} W")
print(f"  Total Losses: {total_losses:.1f} W")

print("\n" + "=" * 80)
print("VALIDATION INSTRUCTIONS")
print("=" * 80)
print("""
To validate this model:

1. Replace the parameters above with values from a real motor datasheet or test report.
2. Run the simulation at the same speed and current as the real test point.
3. Compare:
   - Torque output
   - Efficiency
   - Loss breakdown
4. Adjust model parameters (especially loss factors) until simulation matches real data within acceptable error.

Once validated on known motors, apply similar rigor to experimental motor concepts.
""")
print("=" * 80)