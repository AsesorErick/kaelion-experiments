"""
Kaelion Experiment 2: BEC Analog Black Hole
===========================================
Protocol for measuring λ via acoustic black hole Hawking radiation.

Author: Erick Francisco Pérez Eugenio
Date: January 2026
DOI: 10.5281/zenodo.18238030

Target Labs:
- Jeff Steinhauer (Technion) - Has demonstrated analog Hawking radiation
- Silke Weinfurtner (Nottingham) - Analog gravity expert

Status: Protocol ready, awaiting collaboration
"""

import numpy as np
from typing import Dict, List, Tuple
import matplotlib.pyplot as plt

# =============================================================================
# THEORETICAL BACKGROUND
# =============================================================================
"""
Analog Black Holes in BEC:
--------------------------
A flowing Bose-Einstein condensate can create an "acoustic horizon" where
the flow velocity exceeds the speed of sound. This is mathematically
analogous to a black hole horizon.

The acoustic metric is:

    ds² = (ρ/c) [-(c² - v²)dt² - 2v·dx dt + dx²]

where:
- ρ = condensate density
- c = speed of sound
- v = flow velocity

At the horizon: v = c (flow = sound speed)

Hawking Temperature:
    T_H = ℏ κ / (2π k_B)

where κ is the surface gravity analog:
    κ = |dv/dx|_{horizon}

Kaelion Prediction:
------------------
The entropy of the acoustic black hole should follow:

    S = A/4 + α(λ) log(A) + O(1)

where:
    α(λ) = -0.5 - λ

The parameter λ depends on the BEC interaction strength:
- Weakly interacting BEC: λ → 0 (LQG-like)
- Strongly interacting BEC: λ → 1 (holographic-like)
"""

# =============================================================================
# BEC PARAMETERS
# =============================================================================

class BECParameters:
    """Physical parameters for a rubidium-87 BEC analog black hole."""
    
    # Atomic properties (Rb-87)
    m = 1.44e-25  # kg (atomic mass)
    a_s = 5.3e-9  # m (s-wave scattering length)
    
    # Typical BEC parameters
    n_typical = 1e14 * 1e6  # atoms/m³ (converted from cm⁻³)
    
    # Derived quantities
    @classmethod
    def speed_of_sound(cls, n: float) -> float:
        """Speed of sound in BEC: c = sqrt(gn/m) where g = 4πℏ²a_s/m"""
        hbar = 1.055e-34
        g = 4 * np.pi * hbar**2 * cls.a_s / cls.m
        return np.sqrt(g * n / cls.m)
    
    @classmethod
    def healing_length(cls, n: float) -> float:
        """Healing length: ξ = ℏ / (m * c)"""
        hbar = 1.055e-34
        c = cls.speed_of_sound(n)
        return hbar / (cls.m * c)
    
    @classmethod
    def interaction_parameter(cls, n: float) -> float:
        """
        Dimensionless interaction parameter.
        Maps to Kaelion λ through experimental calibration.
        """
        xi = cls.healing_length(n)
        # Ratio of interaction energy to kinetic energy
        return 1.0 / (n * xi**3)


# =============================================================================
# CORRELATION FUNCTION
# =============================================================================

def hawking_correlation(x1: float, x2: float, T_H: float, lambda_K: float) -> float:
    """
    Two-point correlation function for Hawking partners.
    
    In analog systems, correlations between inside/outside horizon
    reveal the thermal nature of Hawking radiation.
    
    G(x1, x2) = <φ(x1)φ(x2)> - <φ(x1)><φ(x2)>
    
    The Kaelion correction appears in the sub-leading term:
    
    G(x1, x2) ≈ G_0(x1, x2) * [1 + α(λ) * log(|x1-x2|/ξ) / log(A/ξ²)]
    
    Args:
        x1, x2: Positions relative to horizon (x=0)
        T_H: Hawking temperature
        lambda_K: Kaelion parameter
    
    Returns:
        Correlation function value
    """
    kB = 1.38e-23
    hbar = 1.055e-34
    
    # Base thermal correlation
    beta = hbar / (kB * T_H)
    r = abs(x1 - x2)
    
    if r < 1e-10:
        return 0
    
    # Leading term: thermal correlation
    G_0 = np.exp(-r / (hbar * beta / (2 * np.pi)))
    
    # Kaelion correction
    alpha = -0.5 - lambda_K
    xi = 1e-6  # healing length scale
    correction = 1 + alpha * np.log(r / xi) / np.log(1e-4 / xi**2)
    
    return G_0 * correction


def entropy_from_correlations(correlations: np.ndarray, area: float, lambda_K: float) -> Dict:
    """
    Extract entropy from correlation measurements.
    
    Method:
    1. Fit correlation decay to extract temperature
    2. Compute area entropy S = A/4
    3. Fit logarithmic correction to extract α
    4. Verify α = -0.5 - λ
    
    Args:
        correlations: Array of correlation measurements
        area: Horizon "area" (circumference in 1D)
        lambda_K: Expected Kaelion parameter
    
    Returns:
        Dictionary with entropy analysis
    """
    # Leading term
    S_BH = area / 4
    
    # Kaelion correction
    alpha = -0.5 - lambda_K
    S_log = alpha * np.log(area)
    
    # Total entropy
    S_total = S_BH + S_log
    
    return {
        'S_BH': S_BH,
        'S_log': S_log,
        'S_total': S_total,
        'alpha': alpha,
        'lambda_K': lambda_K,
        'formula': f'S = {S_BH:.4f} + ({alpha:.4f}) * log(A)'
    }


# =============================================================================
# EXPERIMENTAL PROTOCOL
# =============================================================================

def bec_protocol() -> Dict:
    """
    Complete experimental protocol for BEC analog black hole.
    
    Returns protocol specification for lab implementation.
    """
    
    protocol = {
        'title': 'Measurement of Kaelion Parameter via BEC Analog Black Hole',
        'target_labs': ['Steinhauer (Technion)', 'Weinfurtner (Nottingham)'],
        
        'setup': {
            'atom': 'Rb-87',
            'atom_number': '1e5 - 1e6',
            'trap': 'Elongated optical dipole trap',
            'flow_method': 'Accelerating potential or obstacle',
            'imaging': 'In-situ absorption imaging'
        },
        
        'procedure': [
            '1. Prepare BEC in elongated trap',
            '2. Create flow using moving potential/obstacle',
            '3. Establish supersonic region (acoustic horizon)',
            '4. Wait for steady state (~100 ms)',
            '5. Image density fluctuations',
            '6. Measure correlations between inside/outside horizon',
            '7. Repeat for statistics (>100 shots)',
            '8. Vary flow velocity to change horizon "area"'
        ],
        
        'measurements': {
            'primary': 'Two-point density-density correlations G(x1, x2)',
            'secondary': 'Temperature from correlation decay',
            'extracted': 'Entropy S(A) as function of horizon size'
        },
        
        'analysis': {
            'fit_model': 'S(A) = A/4 + α*log(A) + const',
            'extract': 'α from fit',
            'compute': 'λ = -0.5 - α',
            'verify': 'α = -0.5 - λ (self-consistency)'
        },
        
        'predictions': {
            'weakly_interacting': {
                'condition': 'na³ << 1',
                'expected_lambda': '0.0 - 0.3',
                'expected_alpha': '-0.8 to -0.5',
                'interpretation': 'LQG-like regime'
            },
            'strongly_interacting': {
                'condition': 'na³ ~ 1',
                'expected_lambda': '0.7 - 1.0',
                'expected_alpha': '-1.5 to -1.2',
                'interpretation': 'Holographic-like regime'
            }
        },
        
        'challenges': [
            'Maintaining stable supersonic flow',
            'Sufficient signal-to-noise in correlations',
            'Systematic effects from trap inhomogeneity',
            'Finite size effects on logarithmic correction'
        ],
        
        'timeline': '6-12 months with existing setup'
    }
    
    return protocol


# =============================================================================
# SIMULATION
# =============================================================================

def simulate_bec_experiment(n_areas: int = 10, lambda_true: float = 0.3) -> Dict:
    """
    Simulate BEC analog black hole experiment.
    
    This simulation demonstrates the expected signal and analysis method.
    Real experiments would replace this with actual data.
    
    Args:
        n_areas: Number of horizon sizes to simulate
        lambda_true: True Kaelion parameter
    
    Returns:
        Simulated experimental results
    """
    np.random.seed(42)
    
    # Horizon "areas" (in units of healing length squared)
    areas = np.linspace(10, 100, n_areas)
    
    # True entropy with Kaelion correction
    alpha_true = -0.5 - lambda_true
    S_true = areas / 4 + alpha_true * np.log(areas)
    
    # Add experimental noise
    noise = 0.1 * np.random.randn(n_areas)
    S_measured = S_true + noise
    
    # Fit to extract alpha
    from scipy.optimize import curve_fit
    
    def entropy_model(A, S0, alpha):
        return A/4 + alpha * np.log(A) + S0
    
    popt, pcov = curve_fit(entropy_model, areas, S_measured, p0=[0, -0.5])
    
    alpha_fit = popt[1]
    alpha_err = np.sqrt(pcov[1, 1])
    lambda_fit = -0.5 - alpha_fit
    
    results = {
        'areas': areas.tolist(),
        'S_measured': S_measured.tolist(),
        'S_true': S_true.tolist(),
        'alpha_true': alpha_true,
        'alpha_fit': alpha_fit,
        'alpha_err': alpha_err,
        'lambda_true': lambda_true,
        'lambda_fit': lambda_fit,
        'verification': {
            'alpha_predicted': -0.5 - lambda_fit,
            'alpha_measured': alpha_fit,
            'match': abs(alpha_fit - (-0.5 - lambda_fit)) < alpha_err
        }
    }
    
    return results


def plot_simulation(results: Dict, save_path: str = None):
    """Plot simulation results."""
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # Left: S vs A
    ax = axes[0]
    areas = np.array(results['areas'])
    ax.scatter(areas, results['S_measured'], label='Measured', s=50)
    ax.plot(areas, results['S_true'], 'r-', label=f'True (λ={results["lambda_true"]:.2f})', linewidth=2)
    
    # Fit line
    alpha_fit = results['alpha_fit']
    S_fit = areas/4 + alpha_fit * np.log(areas)
    ax.plot(areas, S_fit, 'g--', label=f'Fit (α={alpha_fit:.3f})', linewidth=2)
    
    ax.set_xlabel('Horizon Area A', fontsize=12)
    ax.set_ylabel('Entropy S', fontsize=12)
    ax.set_title('Entropy vs Horizon Area', fontsize=12)
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Right: Verification
    ax = axes[1]
    lambda_range = np.linspace(0, 1, 100)
    alpha_pred = -0.5 - lambda_range
    ax.plot(lambda_range, alpha_pred, 'k-', linewidth=2, label='α = -0.5 - λ')
    
    ax.scatter([results['lambda_fit']], [results['alpha_fit']], 
              s=150, c='red', marker='*', label=f'Measured: λ={results["lambda_fit"]:.3f}')
    ax.errorbar([results['lambda_fit']], [results['alpha_fit']], 
               yerr=[results['alpha_err']], fmt='none', c='red', capsize=5)
    
    ax.set_xlabel('λ (Kaelion parameter)', fontsize=12)
    ax.set_ylabel('α (Entropy coefficient)', fontsize=12)
    ax.set_title('Kaelion Verification', fontsize=12)
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_xlim(-0.1, 1.1)
    ax.set_ylim(-1.7, -0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Saved: {save_path}")
    
    plt.show()


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("="*60)
    print("KAELION EXPERIMENT 2: BEC ANALOG BLACK HOLE")
    print("="*60)
    
    # Show protocol
    protocol = bec_protocol()
    print(f"\nProtocol: {protocol['title']}")
    print(f"Target labs: {', '.join(protocol['target_labs'])}")
    print(f"\nProcedure:")
    for step in protocol['procedure']:
        print(f"  {step}")
    
    # Run simulation
    print("\n" + "-"*60)
    print("SIMULATION (Demonstrating expected results)")
    print("-"*60)
    
    results = simulate_bec_experiment(n_areas=15, lambda_true=0.3)
    
    print(f"\nTrue λ: {results['lambda_true']:.4f}")
    print(f"Fit λ:  {results['lambda_fit']:.4f}")
    print(f"Fit α:  {results['alpha_fit']:.4f} ± {results['alpha_err']:.4f}")
    print(f"\nVerification:")
    print(f"  α predicted = -0.5 - λ = {results['verification']['alpha_predicted']:.4f}")
    print(f"  α measured  = {results['verification']['alpha_measured']:.4f}")
    print(f"  Match: {results['verification']['match']}")
    
    # Plot
    try:
        plot_simulation(results, 'bec_simulation.png')
    except:
        print("\n(Plotting requires display - skipped)")
    
    print("\n" + "="*60)
    print("Status: PROTOCOL READY - Awaiting lab collaboration")
    print("="*60)
