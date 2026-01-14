"""
KAELION EXPERIMENT 2: BEC ANALOG GRAVITY
=========================================
Experimental protocol for measuring λ in Bose-Einstein Condensate
analog black holes.

Target labs:
- Jeff Steinhauer (Technion)
- Silke Weinfurtner (Nottingham)
- Ulf Leonhardt (Weizmann)

Author: Erick Francisco Pérez Eugenio
Date: January 2026
"""

import numpy as np
import matplotlib.pyplot as plt

print("="*70)
print("KAELION EXPERIMENT 2: BEC ANALOG GRAVITY")
print("Measuring λ in Analog Black Holes")
print("="*70)

# =============================================================================
# EXPERIMENTAL PROTOCOL
# =============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║              BEC ANALOG BLACK HOLE EXPERIMENT                        ║
║                                                                      ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  PRINCIPLE:                                                          ║
║    Supersonic flow in BEC creates acoustic horizon                  ║
║    Phonons cannot escape → Analog of event horizon                  ║
║    Hawking radiation → Correlated phonon pairs                      ║
║                                                                      ║
║  KAELION PREDICTION:                                                 ║
║    Entropy of acoustic horizon follows:                             ║
║    S = A/4 + α(λ)·log(A)                                           ║
║    where A = horizon "area" (perimeter in 1D)                       ║
║                                                                      ║
║  MEASURABLE:                                                         ║
║    • Hawking temperature T_H                                        ║
║    • Correlation functions                                          ║
║    • Entanglement entropy                                           ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
""")

# =============================================================================
# PART 1: BEC SYSTEM SETUP
# =============================================================================

print("\n" + "="*70)
print("PART 1: BEC SYSTEM SETUP")
print("="*70)

class BECAnalogBlackHole:
    """
    Model BEC analog black hole.
    """
    
    def __init__(self, c_sound=1.0, v_flow=1.5):
        """
        c_sound: Speed of sound in BEC
        v_flow: Flow velocity (must exceed c for horizon)
        """
        self.c = c_sound
        self.v = v_flow
        
        # Horizon exists if v > c
        self.has_horizon = v_flow > c_sound
        
    def surface_gravity(self):
        """
        Surface gravity κ at acoustic horizon.
        κ = (1/2) |d(v² - c²)/dx| at horizon
        
        Simplified: κ ≈ (v - c) / ξ
        where ξ = healing length
        """
        if not self.has_horizon:
            return 0
        xi = 0.1  # Healing length (typical BEC scale)
        return (self.v - self.c) / xi
    
    def hawking_temperature(self):
        """
        Analog Hawking temperature.
        T_H = ℏκ / (2πk_B)
        
        In natural units: T_H = κ / (2π)
        """
        kappa = self.surface_gravity()
        return kappa / (2 * np.pi)
    
    def horizon_perimeter(self, width=10.0):
        """
        "Area" of acoustic horizon (perimeter in quasi-1D).
        """
        return width  # In 1D, "area" is just the transverse width
    
    def entropy_kaelion(self, lambda_param, width=10.0):
        """
        Kaelion entropy formula for analog horizon.
        """
        A = self.horizon_perimeter(width)
        alpha = -0.5 - lambda_param
        return A/4 + alpha * np.log(A)
    
    def entanglement_entropy(self, subsystem_size):
        """
        Entanglement entropy between inside/outside horizon.
        Should follow area law with log corrections.
        """
        # Area law in 1D: S ~ const + (c/3) log(L)
        # The coefficient maps to α
        c_central = 1.0  # Central charge
        S = (c_central / 3) * np.log(subsystem_size + 1)
        return S


bec = BECAnalogBlackHole(c_sound=1.0, v_flow=1.5)

print(f"BEC Parameters:")
print(f"  Speed of sound: c = {bec.c}")
print(f"  Flow velocity: v = {bec.v}")
print(f"  Horizon exists: {bec.has_horizon}")
print(f"  Surface gravity: κ = {bec.surface_gravity():.3f}")
print(f"  Hawking temperature: T_H = {bec.hawking_temperature():.4f}")


# =============================================================================
# PART 2: MEASUREMENT PROTOCOL
# =============================================================================

print("\n" + "="*70)
print("PART 2: MEASUREMENT PROTOCOL")
print("="*70)

print("""
MEASUREMENT STEPS:

1. CREATE ACOUSTIC HORIZON
   • Prepare BEC in harmonic trap
   • Create supersonic flow using potential step
   • Verify horizon formation via density imaging

2. MEASURE HAWKING RADIATION
   • Detect correlated phonon pairs
   • Use density-density correlations: <n(x)n(x')>
   • Extract Hawking temperature from spectrum

3. MEASURE ENTANGLEMENT ENTROPY
   • Partition system: inside horizon / outside
   • Measure correlation matrix
   • Compute entanglement entropy from eigenvalues

4. VARY HORIZON SIZE
   • Change flow velocity → change horizon position
   • Measure S for different "areas" A
   • Fit to S = A/4 + α·log(A)

5. EXTRACT λ
   • From fitted α: λ = -0.5 - α
   • Compare with theoretical predictions
""")


# =============================================================================
# PART 3: DATA ANALYSIS
# =============================================================================

print("\n" + "="*70)
print("PART 3: DATA ANALYSIS")
print("="*70)

class BECDataAnalysis:
    """
    Analyze BEC experiment data to extract λ.
    """
    
    def __init__(self):
        pass
    
    def fit_entropy_vs_area(self, areas, entropies):
        """
        Fit S = A/4 + α·log(A) + const
        """
        from scipy.optimize import curve_fit
        
        def entropy_model(A, alpha, const):
            return A/4 + alpha * np.log(A) + const
        
        try:
            popt, pcov = curve_fit(entropy_model, areas, entropies, 
                                   p0=[-1.0, 0.0], maxfev=5000)
            alpha = popt[0]
            error = np.sqrt(pcov[0, 0])
            return alpha, error
        except:
            return None, None
    
    def extract_lambda(self, alpha):
        """
        Convert α to λ.
        """
        return -0.5 - alpha
    
    def correlation_to_temperature(self, g2_data, distance):
        """
        Extract temperature from g² correlations.
        """
        # g²(x, x') ~ exp(-|x-x'|/ξ_T)
        # ξ_T = ℏc/(k_B T)
        pass


# Simulate expected data
np.random.seed(42)

areas = np.linspace(5, 50, 10)
lambda_true = 0.6
alpha_true = -0.5 - lambda_true

# Generate synthetic data
entropies = areas/4 + alpha_true * np.log(areas) + np.random.normal(0, 0.1, len(areas))

analysis = BECDataAnalysis()
alpha_fit, error = analysis.fit_entropy_vs_area(areas, entropies)
lambda_fit = analysis.extract_lambda(alpha_fit)

print(f"\nSimulated Data Analysis:")
print(f"  True λ = {lambda_true}")
print(f"  True α = {alpha_true}")
print(f"  Fitted α = {alpha_fit:.3f} ± {error:.3f}")
print(f"  Extracted λ = {lambda_fit:.3f}")
print(f"  Match: {abs(lambda_fit - lambda_true) < 0.1}")


# =============================================================================
# PART 4: EXPECTED RESULTS BY REGIME
# =============================================================================

print("\n" + "="*70)
print("PART 4: EXPECTED RESULTS BY REGIME")
print("="*70)

print("""
KAELION PREDICTIONS FOR BEC:

1. STRONGLY INTERACTING BEC (more discrete)
   • Expected: λ → 0 (LQG-like)
   • α → -0.5
   • Signatures: Strong quantum fluctuations

2. WEAKLY INTERACTING BEC (more classical/continuous)
   • Expected: λ → 1 (holographic-like)
   • α → -1.5
   • Signatures: Mean-field behavior

3. INTERMEDIATE REGIME
   • Expected: λ ~ 0.5
   • α ~ -1.0
   • Most experimentally accessible
""")

# Table of predictions
print(f"\n{'Regime':<25} {'Expected λ':<15} {'Expected α':<15}")
print("-" * 55)
regimes = [
    ('Strong interactions', 0.2, -0.7),
    ('Intermediate', 0.5, -1.0),
    ('Weak interactions', 0.8, -1.3),
]
for regime, lam, alpha in regimes:
    print(f"{regime:<25} {lam:<15.1f} {alpha:<15.1f}")


# =============================================================================
# PART 5: CONTACT INFORMATION FOR LABS
# =============================================================================

print("\n" + "="*70)
print("PART 5: TARGET LABORATORIES")
print("="*70)

print("""
LABORATORIES WITH BEC ANALOG GRAVITY EXPERTISE:

1. JEFF STEINHAUER GROUP (Technion, Israel)
   • First observation of analog Hawking radiation (2016)
   • Demonstrated stimulated Hawking effect (2019)
   • Email: jeffs@technion.ac.il
   • IDEAL FOR: Hawking temperature, correlations

2. SILKE WEINFURTNER GROUP (Nottingham, UK)
   • Rotating superfluid black holes
   • Superradiance experiments
   • Email: silke.weinfurtner@nottingham.ac.uk
   • IDEAL FOR: Different geometries, superradiance

3. ULF LEONHARDT GROUP (Weizmann, Israel)
   • Optical analog black holes
   • Fiber optic event horizons
   • IDEAL FOR: Optical implementation

4. IACOPO CARUSOTTO GROUP (Trento, Italy)
   • Theoretical support for BEC analogs
   • Quantum fluctuations calculations
   • IDEAL FOR: Theory collaboration

PROPOSED COLLABORATION EMAIL TEMPLATE:

Subject: Kaelion correspondence verification in BEC analog black holes

Dear Prof. [Name],

We have developed a theoretical framework called the "Kaelion 
correspondence" that predicts specific logarithmic corrections 
to black hole entropy, with parameter λ interpolating between 
LQG (λ=0) and holographic (λ=1) limits.

Your BEC analog black hole experiments could provide the first 
experimental test. Specifically, we predict:

S = A/4 + α(λ)·log(A), where α = -0.5 - λ

We have prepared detailed experimental protocols and would be 
honored to collaborate.

GitHub: github.com/AsesorErick/kaelion-derivation
DOI: 10.5281/zenodo.18245761

Best regards,
Erick Francisco Pérez Eugenio
""")


# =============================================================================
# PART 6: VISUALIZATION
# =============================================================================

print("\n" + "="*70)
print("GENERATING VISUALIZATION")
print("="*70)

fig, axes = plt.subplots(2, 2, figsize=(12, 10))
fig.suptitle('KAELION EXPERIMENT 2: BEC ANALOG GRAVITY\nMeasuring λ in Acoustic Black Holes', 
             fontsize=14, fontweight='bold')

# 1. BEC flow profile
ax1 = axes[0, 0]
x = np.linspace(-5, 5, 100)
v_profile = 1.5 * (1 + 0.3 * np.tanh(x))
c_profile = np.ones_like(x)
ax1.plot(x, v_profile, 'b-', linewidth=2, label='Flow velocity v')
ax1.plot(x, c_profile, 'r--', linewidth=2, label='Sound speed c')
ax1.axvline(0, color='green', linestyle=':', label='Horizon (v=c)')
ax1.fill_between(x, v_profile, c_profile, where=v_profile>c_profile, 
                  alpha=0.3, color='gray', label='Supersonic region')
ax1.set_xlabel('Position x')
ax1.set_ylabel('Velocity')
ax1.set_title('Acoustic Horizon Formation')
ax1.legend(loc='upper left')
ax1.grid(True, alpha=0.3)

# 2. Entropy vs Area
ax2 = axes[0, 1]
ax2.scatter(areas, entropies, s=50, label='Simulated data')
A_fit = np.linspace(5, 50, 100)
S_fit = A_fit/4 + alpha_fit * np.log(A_fit)
ax2.plot(A_fit, S_fit, 'r-', linewidth=2, label=f'Fit: α = {alpha_fit:.2f}')
ax2.set_xlabel('Horizon "Area" A')
ax2.set_ylabel('Entropy S')
ax2.set_title('Entropy vs Area (Kaelion Fit)')
ax2.legend()
ax2.grid(True, alpha=0.3)

# 3. Hawking spectrum
ax3 = axes[1, 0]
omega = np.linspace(0.1, 5, 100)
T_H = bec.hawking_temperature()
planck = 1 / (np.exp(omega / T_H) - 1)
ax3.plot(omega, planck, 'purple', linewidth=2)
ax3.set_xlabel('Frequency ω')
ax3.set_ylabel('Occupation number')
ax3.set_title(f'Hawking Spectrum (T_H = {T_H:.3f})')
ax3.grid(True, alpha=0.3)

# 4. Summary
ax4 = axes[1, 1]
ax4.axis('off')
summary = """
BEC EXPERIMENT SUMMARY

SYSTEM:
• Supersonic BEC flow
• Acoustic horizon at v = c
• Analog Hawking radiation

MEASUREMENTS:
• Density correlations <n(x)n(x')>
• Entanglement entropy
• Hawking temperature

KAELION PREDICTION:
S = A/4 + α(λ)·log(A)
α = -0.5 - λ

EXPECTED λ:
• Strong coupling: λ ~ 0.2
• Weak coupling: λ ~ 0.8

TARGET LABS:
• Steinhauer (Technion)
• Weinfurtner (Nottingham)

STATUS: Protocol ready
"""
ax4.text(0.1, 0.9, summary, transform=ax4.transAxes, fontsize=10,
         verticalalignment='top', family='monospace',
         bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.5))

plt.tight_layout()
plt.savefig('Experiment2_BEC.png', dpi=150, bbox_inches='tight')
print("Figure saved: Experiment2_BEC.png")
plt.close()


# =============================================================================
# CONCLUSIONS
# =============================================================================

print("\n" + "="*70)
print("CONCLUSIONS")
print("="*70)

print("""
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║                 BEC EXPERIMENT - PROTOCOL READY                      ║
║                                                                      ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  PROTOCOL COMPLETE:                                                  ║
║    ✓ System setup (supersonic BEC flow)                             ║
║    ✓ Measurement procedure (correlations, entropy)                  ║
║    ✓ Data analysis (fit S = A/4 + α·log(A))                        ║
║    ✓ Target laboratories identified                                 ║
║                                                                      ║
║  KAELION PREDICTIONS:                                                ║
║    • Strong interactions: λ ~ 0.2, α ~ -0.7                         ║
║    • Weak interactions: λ ~ 0.8, α ~ -1.3                           ║
║    • Intermediate: λ ~ 0.5, α ~ -1.0                                ║
║                                                                      ║
║  FALSIFIABLE:                                                        ║
║    If α ∉ [-1.5, -0.5] or α ≠ -0.5 - λ,                            ║
║    Kaelion is FALSIFIED.                                            ║
║                                                                      ║
║  NEXT STEPS:                                                         ║
║    1. Contact Steinhauer group                                      ║
║    2. Share protocol                                                ║
║    3. Collaborate on experiment                                     ║
║    4. Analyze data with Kaelion framework                          ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
""")

print("="*70)
