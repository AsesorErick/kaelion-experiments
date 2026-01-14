"""
Kaelion Experiment 1: Quantum Circuit OTOC
==========================================
Protocol for measuring λ via OTOC decay on quantum hardware.

This is the PROTOCOL file. For actual experimental results, see:
  ibm_quantum_otoc/

Author: Erick Francisco Pérez Eugenio
Date: January 2026
DOI: 10.5281/zenodo.18238030
"""

import numpy as np
from typing import List, Tuple, Dict

# =============================================================================
# THEORETICAL BACKGROUND
# =============================================================================
"""
The Out-of-Time-Order Correlator (OTOC) measures quantum information scrambling:

    F(t) = <W†(t) V† W(t) V>

For chaotic systems, F(t) decays exponentially:

    F(t) ~ exp(-λ_L * t)

where λ_L is the quantum Lyapunov exponent, bounded by:

    λ_L ≤ 2π T / ℏ  (MSS bound)

The Kaelion parameter is defined as:

    λ = λ_L / (2π T_eff)

with the prediction:

    α(λ) = -0.5 - λ

where α is the coefficient of logarithmic corrections to entropy.
"""

# =============================================================================
# CIRCUIT DEFINITIONS
# =============================================================================

def create_chaotic_layer(n_qubits: int, seed: int = None) -> List[Tuple]:
    """
    Creates a chaotic layer with random rotations + entangling gates.
    
    Chaotic dynamics emerge from:
    1. Random single-qubit rotations (breaks integrability)
    2. All-to-all entanglement (spreads information)
    
    Returns list of (gate_type, params, qubits) tuples.
    """
    if seed is not None:
        np.random.seed(seed)
    
    gates = []
    
    # Random rotations on each qubit
    for i in range(n_qubits):
        theta = np.random.uniform(0, 2*np.pi)
        phi = np.random.uniform(0, 2*np.pi)
        gates.append(('U', (theta, phi, 0), [i]))
    
    # Cyclic CNOT chain (creates entanglement)
    for i in range(n_qubits - 1):
        gates.append(('CNOT', None, [i, i+1]))
    gates.append(('CNOT', None, [n_qubits-1, 0]))  # Close the cycle
    
    return gates


def create_integrable_layer(n_qubits: int) -> List[Tuple]:
    """
    Creates an integrable layer with Clifford gates only.
    
    Integrable dynamics:
    1. Hadamard gates (creates superposition)
    2. Linear CNOT chain (limited entanglement spread)
    
    No chaos - information remains localized.
    """
    gates = []
    
    # Hadamard on each qubit
    for i in range(n_qubits):
        gates.append(('H', None, [i]))
    
    # Linear CNOT chain
    for i in range(n_qubits - 1):
        gates.append(('CNOT', None, [i, i+1]))
    
    return gates


def create_intermediate_layer(n_qubits: int) -> List[Tuple]:
    """
    Creates an intermediate layer (partial chaos).
    
    Intermediate dynamics:
    1. H + T gates (non-Clifford but structured)
    2. Linear CNOT chain
    
    Some scrambling, but not maximal.
    """
    gates = []
    
    for i in range(n_qubits):
        gates.append(('H', None, [i]))
        gates.append(('T', None, [i]))
    
    for i in range(n_qubits - 1):
        gates.append(('CNOT', None, [i, i+1]))
    
    return gates


# =============================================================================
# OTOC PROTOCOL
# =============================================================================

def otoc_protocol(n_qubits: int, depth: int, circuit_type: str, seed: int = 42) -> Dict:
    """
    Complete OTOC measurement protocol.
    
    Protocol:
    1. Prepare |ψ⟩ = H|0⟩ on qubit 0
    2. Apply V = X on qubit 0
    3. Forward evolution U(t) for 'depth' layers
    4. Apply W = Z on last qubit
    5. Backward evolution U†(t)
    6. Apply V† = X on qubit 0
    7. Measure in computational basis
    
    OTOC = P(|0...0⟩)
    
    Args:
        n_qubits: Number of qubits
        depth: Number of evolution layers
        circuit_type: 'chaotic', 'integrable', or 'intermediate'
        seed: Random seed (use seed + depth*100 for unique seeds per depth)
    
    Returns:
        Dictionary with circuit specification
    """
    
    circuit = {
        'n_qubits': n_qubits,
        'depth': depth,
        'type': circuit_type,
        'seed': seed,
        'gates': []
    }
    
    # 1. Prepare superposition
    circuit['gates'].append(('H', None, [0]))
    
    # 2. Apply V = X
    circuit['gates'].append(('X', None, [0]))
    
    # 3. Forward evolution
    for d in range(depth):
        layer_seed = seed + d * 100 if circuit_type == 'chaotic' else None
        
        if circuit_type == 'chaotic':
            layer = create_chaotic_layer(n_qubits, layer_seed)
        elif circuit_type == 'integrable':
            layer = create_integrable_layer(n_qubits)
        else:
            layer = create_intermediate_layer(n_qubits)
        
        circuit['gates'].extend(layer)
    
    # 4. Apply W = Z
    circuit['gates'].append(('Z', None, [n_qubits - 1]))
    
    # 5. Backward evolution (inverse)
    # Note: In actual implementation, use qc.inverse() on forward evolution
    circuit['gates'].append(('INVERSE_EVOLUTION', None, None))
    
    # 6. Apply V† = X
    circuit['gates'].append(('X', None, [0]))
    
    # 7. Measure
    circuit['gates'].append(('MEASURE', None, list(range(n_qubits))))
    
    return circuit


# =============================================================================
# ANALYSIS
# =============================================================================

def extract_lambda(depths: List[int], otoc_values: List[float], T_eff: float = 0.5) -> Dict:
    """
    Extract Kaelion parameter λ from OTOC decay data.
    
    Fits OTOC(d) = A * exp(-λ_L * d) + B
    Then computes λ = λ_L / (2π T_eff)
    
    Args:
        depths: List of circuit depths
        otoc_values: Corresponding OTOC measurements
        T_eff: Effective temperature (default 0.5)
    
    Returns:
        Dictionary with extracted parameters
    """
    from scipy.optimize import curve_fit
    
    def decay_model(t, A, lam, B):
        return A * np.exp(-lam * t) + B
    
    try:
        popt, pcov = curve_fit(
            decay_model,
            np.array(depths),
            np.array(otoc_values),
            p0=[1.0, 0.2, 0.0],
            bounds=([0, 0, -0.5], [2, 5, 0.5])
        )
        
        lambda_L = popt[1]
        lambda_L_err = np.sqrt(pcov[1, 1]) if pcov[1, 1] > 0 else 0
        
        mss_bound = 2 * np.pi * T_eff
        lambda_K = np.clip(lambda_L / mss_bound, 0, 1)
        alpha = -0.5 - lambda_K
        
        return {
            'lambda_L': lambda_L,
            'lambda_L_err': lambda_L_err,
            'lambda_K': lambda_K,
            'alpha': alpha,
            'alpha_predicted': -0.5 - lambda_K,
            'fit_params': {'A': popt[0], 'lambda': popt[1], 'B': popt[2]},
            'success': True
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


# =============================================================================
# PREDICTIONS
# =============================================================================

PREDICTIONS = {
    'chaotic': {
        'lambda_range': (0.7, 1.0),
        'alpha_range': (-1.5, -1.2),
        'interpretation': 'Holographic limit - maximal scrambling'
    },
    'integrable': {
        'lambda_range': (0.0, 0.3),
        'alpha_range': (-0.8, -0.5),
        'interpretation': 'LQG limit - no scrambling'
    },
    'intermediate': {
        'lambda_range': (0.3, 0.6),
        'alpha_range': (-1.1, -0.8),
        'interpretation': 'Interpolation regime'
    }
}


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("="*60)
    print("KAELION EXPERIMENT 1: QUANTUM CIRCUIT OTOC")
    print("="*60)
    print("\nThis file contains the PROTOCOL definition.")
    print("\nFor actual experimental results on IBM Quantum hardware,")
    print("see: ibm_quantum_otoc/")
    print("\nPredictions:")
    print("-"*60)
    for ctype, pred in PREDICTIONS.items():
        print(f"\n{ctype.upper()}:")
        print(f"  Expected λ: {pred['lambda_range']}")
        print(f"  Expected α: {pred['alpha_range']}")
        print(f"  Interpretation: {pred['interpretation']}")
    print("\n" + "="*60)
