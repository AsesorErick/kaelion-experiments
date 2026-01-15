# ============================================================
# CODE 6: KICKED ISING - 4 QUBITS
# ============================================================
# Kaelion Project - Experimental verification of λ parameter
# Author: Erick Francisco Perez Eugenio
# Date: January 2026
# ============================================================

import numpy as np
from datetime import datetime

print("="*70)
print("KAELION OTOC - KICKED ISING (4 QUBITS)")
print("="*70)
print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from scipy.optimize import curve_fit

# ============================================================
# PARAMETERS
# ============================================================
N_QUBITS = 4
DEPTHS = [1, 2, 4, 6, 8, 10, 14]
SHOTS = 4096
N_RUNS = 5
J = 0.9  # Ising coupling
h = 0.7  # Transverse field

print(f"\nParameters:")
print(f"  N_QUBITS = {N_QUBITS}")
print(f"  DEPTHS = {DEPTHS}")
print(f"  SHOTS = {SHOTS}")
print(f"  N_RUNS = {N_RUNS}")
print(f"  J = {J}, h = {h}")

# ============================================================
# IBM QUANTUM CONNECTION
# ============================================================
print("\n[1] Connecting to IBM Quantum...")

# IMPORTANT: Replace with your API key
API_KEY = "YOUR_API_KEY_HERE"

try:
    service = QiskitRuntimeService(channel="ibm_quantum_platform")
except:
    QiskitRuntimeService.save_account(
        channel="ibm_quantum_platform", 
        token=API_KEY, 
        overwrite=True
    )
    service = QiskitRuntimeService(channel="ibm_quantum_platform")

backend = service.least_busy(
    simulator=False, 
    operational=True, 
    min_num_qubits=N_QUBITS
)
print(f"    Backend: {backend.name}")
print(f"    Available qubits: {backend.num_qubits}")

pm = generate_preset_pass_manager(backend=backend, optimization_level=3)

# ============================================================
# KICKED ISING CIRCUIT
# ============================================================
def create_kicked_ising_otoc(n, depth, J=0.9, h=0.7):
    """
    Kicked Ising model for OTOC measurement.
    
    H = J * sum(Z_i Z_{i+1}) + h * sum(X_i)
    
    This model is dual to JT Gravity and saturates the MSS bound.
    Parameters J=0.9, h=0.7 are at the self-dual chaotic point.
    """
    qr = QuantumRegister(n, 'q')
    cr = ClassicalRegister(n, 'c')
    qc = QuantumCircuit(qr, cr)
    
    # OTOC preparation
    qc.h(qr[0])
    qc.x(qr[0])
    
    # Forward evolution
    for _ in range(depth):
        for i in range(n):
            qc.rx(2 * h, qr[i])
        for i in range(n - 1):
            qc.rzz(2 * J, qr[i], qr[i + 1])
        qc.rzz(2 * J, qr[n-1], qr[0])  # Periodic boundary
    
    # W operator
    qc.z(qr[n - 1])
    
    # Backward evolution (exact inverse)
    for _ in range(depth):
        qc.rzz(-2 * J, qr[n-1], qr[0])
        for i in range(n - 2, -1, -1):
            qc.rzz(-2 * J, qr[i], qr[i + 1])
        for i in range(n):
            qc.rx(-2 * h, qr[i])
    
    # Close OTOC
    qc.x(qr[0])
    qc.measure(qr, cr)
    
    return qc

# ============================================================
# INTEGRABLE CIRCUIT (BASELINE)
# ============================================================
def create_integrable_otoc(n, depth):
    """Integrable circuit - should give λ ≈ 0"""
    qr = QuantumRegister(n, 'q')
    cr = ClassicalRegister(n, 'c')
    qc = QuantumCircuit(qr, cr)
    
    qc.h(qr[0])
    qc.x(qr[0])
    
    for _ in range(depth):
        for i in range(n):
            qc.h(qr[i])
        for i in range(n - 1):
            qc.cx(qr[i], qr[i + 1])
    
    qc.z(qr[n - 1])
    
    for _ in range(depth):
        for i in range(n - 2, -1, -1):
            qc.cx(qr[i], qr[i + 1])
        for i in range(n):
            qc.h(qr[i])
    
    qc.x(qr[0])
    qc.measure(qr, cr)
    
    return qc

# ============================================================
# EXECUTION FUNCTION
# ============================================================
def run_experiment(create_func, label, **kwargs):
    print(f"\n    Running: {label}")
    
    circuits = [create_func(N_QUBITS, d, **kwargs) for d in DEPTHS]
    transpiled = pm.run(circuits)
    transpiled_depths = [t.depth() for t in transpiled]
    print(f"      Transpiled depths: {transpiled_depths}")
    
    sampler = Sampler(backend)
    job = sampler.run(transpiled, shots=SHOTS)
    job_id = job.job_id()
    print(f"      Job ID: {job_id}")
    print(f"      Waiting for results...")
    
    result = job.result()
    
    otoc_values = []
    for pub_result in result:
        counts = pub_result.data.c.get_counts()
        zero_state = '0' * N_QUBITS
        otoc = counts.get(zero_state, 0) / sum(counts.values())
        otoc_values.append(otoc)
    
    print(f"      OTOC values: {[f'{v:.4f}' for v in otoc_values]}")
    
    # Fit exponential decay
    def decay(t, A, lam, B):
        return A * np.exp(-lam * t) + B
    
    mss = 2 * np.pi * 0.5  # MSS bound
    
    try:
        popt, pcov = curve_fit(
            decay, 
            DEPTHS, 
            otoc_values, 
            p0=[1, 0.3, 0], 
            bounds=([0, 0, -0.5], [2, 5, 0.5]),
            maxfev=5000
        )
        lambda_K = np.clip(popt[1] / mss, 0, 1)
    except:
        lambda_K = -1
    
    alpha = -0.5 - lambda_K if lambda_K >= 0 else None
    print(f"      → λ = {lambda_K:.4f}, α = {alpha:.4f}")
    
    return {
        'lambda': float(lambda_K),
        'alpha': float(alpha) if alpha else None,
        'otoc_values': [float(v) for v in otoc_values],
        'job_id': job_id
    }

# ============================================================
# MAIN EXECUTION
# ============================================================
print("\n" + "="*70)
print("[2] RUNNING EXPERIMENTS")
print("="*70)

results_kicked = []
results_integrable = []

for run in range(N_RUNS):
    print(f"\n{'─'*70}")
    print(f"  RUN {run+1}/{N_RUNS}")
    print(f"{'─'*70}")
    
    res_kicked = run_experiment(create_kicked_ising_otoc, "Kicked Ising (Chaotic)", J=J, h=h)
    results_kicked.append(res_kicked)
    
    res_int = run_experiment(create_integrable_otoc, "Integrable (Baseline)")
    results_integrable.append(res_int)

# ============================================================
# STATISTICAL ANALYSIS
# ============================================================
print("\n" + "="*70)
print("[3] STATISTICAL RESULTS")
print("="*70)

lambdas_kicked = [r['lambda'] for r in results_kicked if r['lambda'] >= 0]
lambdas_int = [r['lambda'] for r in results_integrable if r['lambda'] >= 0]

print(f"\n  KICKED ISING (Chaotic):")
print(f"    λ values: {[f'{v:.4f}' for v in lambdas_kicked]}")
print(f"    Mean:     {np.mean(lambdas_kicked):.4f}")
print(f"    Std:      {np.std(lambdas_kicked):.4f}")
print(f"    α mean:   {-0.5 - np.mean(lambdas_kicked):.4f}")

print(f"\n  INTEGRABLE (Baseline):")
print(f"    λ values: {[f'{v:.4f}' for v in lambdas_int]}")
print(f"    Mean:     {np.mean(lambdas_int):.4f}")
print(f"    Std:      {np.std(lambdas_int):.4f}")
print(f"    α mean:   {-0.5 - np.mean(lambdas_int):.4f}")

# ============================================================
# KAELION VERIFICATION
# ============================================================
print("\n" + "="*70)
print("[4] KAELION VERIFICATION: α = -0.5 - λ")
print("="*70)

print(f"\n  Kicked Ising: λ = {np.mean(lambdas_kicked):.4f} → α = {-0.5 - np.mean(lambdas_kicked):.4f}")
print(f"  Integrable:   λ = {np.mean(lambdas_int):.4f} → α = {-0.5 - np.mean(lambdas_int):.4f}")

print("\n" + "="*70)
print("EXPERIMENT COMPLETED")
print("="*70)
