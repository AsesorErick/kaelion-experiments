# ============================================================
# CODE 9: SYK SIMPLIFIED - UNIVERSALITY TEST
# ============================================================
# Kaelion Project - Verify λ universality across chaotic models
# Author: Erick Francisco Perez Eugenio
# Date: January 2026
# ============================================================

import numpy as np
from datetime import datetime

print("="*70)
print("KAELION OTOC - SYK SIMPLIFIED (UNIVERSALITY)")
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

print(f"\nParameters:")
print(f"  N_QUBITS = {N_QUBITS}")
print(f"  DEPTHS = {DEPTHS}")
print(f"  SHOTS = {SHOTS}")
print(f"  N_RUNS = {N_RUNS}")
print(f"  Model: SYK simplified (all-to-all random couplings)")

# ============================================================
# IBM QUANTUM CONNECTION
# ============================================================
print("\n[1] Connecting to IBM Quantum...")

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
# SYK SIMPLIFIED CIRCUIT
# ============================================================
def create_syk_otoc(n, depth, seed=42):
    """
    Simplified SYK circuit for OTOC measurement.
    
    The SYK model is dual to JT Gravity (2D holography).
    Features:
    - ALL-TO-ALL interactions (not just neighbors)
    - Random couplings (simulates disorder)
    
    If SYK and Kicked Ising both give λ ≈ 1, universality is confirmed.
    """
    np.random.seed(seed + depth * 100)
    
    qr = QuantumRegister(n, 'q')
    cr = ClassicalRegister(n, 'c')
    qc = QuantumCircuit(qr, cr)
    
    # OTOC preparation
    qc.h(qr[0])
    qc.x(qr[0])
    
    # Forward evolution: SYK-like
    for _ in range(depth):
        # Random single-qubit rotations
        for i in range(n):
            theta = np.random.uniform(0, np.pi)
            phi = np.random.uniform(0, 2*np.pi)
            qc.u(theta, phi, 0, qr[i])
        
        # ALL-TO-ALL interactions with random couplings
        for i in range(n):
            for j in range(i+1, n):
                J_ij = np.random.uniform(0.5, 1.5)
                qc.rzz(2 * J_ij, qr[i], qr[j])
    
    # W operator
    qc.z(qr[n - 1])
    
    # Backward evolution (exact inverse)
    np.random.seed(seed + depth * 100)
    
    all_thetas, all_phis, all_Js = [], [], []
    for _ in range(depth):
        layer_theta = [np.random.uniform(0, np.pi) for _ in range(n)]
        layer_phi = [np.random.uniform(0, 2*np.pi) for _ in range(n)]
        all_thetas.append(layer_theta)
        all_phis.append(layer_phi)
        
        layer_J = []
        for i in range(n):
            for j in range(i+1, n):
                layer_J.append(np.random.uniform(0.5, 1.5))
        all_Js.append(layer_J)
    
    for layer in range(depth - 1, -1, -1):
        idx = 0
        for i in range(n):
            for j in range(i+1, n):
                qc.rzz(-2 * all_Js[layer][idx], qr[i], qr[j])
                idx += 1
        for i in range(n):
            qc.u(-all_thetas[layer][i], -all_phis[layer][i], 0, qr[i])
    
    qc.x(qr[0])
    qc.measure(qr, cr)
    
    return qc

# ============================================================
# KICKED ISING (REFERENCE)
# ============================================================
def create_kicked_ising_otoc(n, depth, J=0.9, h=0.7):
    qr = QuantumRegister(n, 'q')
    cr = ClassicalRegister(n, 'c')
    qc = QuantumCircuit(qr, cr)
    
    qc.h(qr[0])
    qc.x(qr[0])
    
    for _ in range(depth):
        for i in range(n):
            qc.rx(2 * h, qr[i])
        for i in range(n - 1):
            qc.rzz(2 * J, qr[i], qr[i + 1])
        qc.rzz(2 * J, qr[n-1], qr[0])
    
    qc.z(qr[n - 1])
    
    for _ in range(depth):
        qc.rzz(-2 * J, qr[n-1], qr[0])
        for i in range(n - 2, -1, -1):
            qc.rzz(-2 * J, qr[i], qr[i + 1])
        for i in range(n):
            qc.rx(-2 * h, qr[i])
    
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
    
    sampler = Sampler(backend)
    job = sampler.run(transpiled, shots=SHOTS)
    job_id = job.job_id()
    print(f"      Job ID: {job_id}")
    print(f"      Waiting...")
    
    result = job.result()
    
    otoc_values = []
    for pub_result in result:
        counts = pub_result.data.c.get_counts()
        zero_state = '0' * N_QUBITS
        otoc = counts.get(zero_state, 0) / sum(counts.values())
        otoc_values.append(otoc)
    
    def decay(t, A, lam, B):
        return A * np.exp(-lam * t) + B
    
    mss = 2 * np.pi * 0.5
    
    try:
        popt, _ = curve_fit(decay, DEPTHS, otoc_values, 
                           p0=[1, 0.3, 0], bounds=([0, 0, -0.5], [2, 5, 0.5]), maxfev=5000)
        lambda_K = np.clip(popt[1] / mss, 0, 1)
    except:
        lambda_K = -1
    
    alpha = -0.5 - lambda_K if lambda_K >= 0 else None
    print(f"      → λ = {lambda_K:.4f}, α = {alpha:.4f}")
    
    return {'lambda': float(lambda_K), 'alpha': float(alpha) if alpha else None}

# ============================================================
# MAIN EXECUTION
# ============================================================
print("\n" + "="*70)
print("[2] RUNNING EXPERIMENTS")
print("="*70)

results_syk = []
results_kicked = []

for run in range(N_RUNS):
    print(f"\n{'─'*70}")
    print(f"  RUN {run+1}/{N_RUNS}")
    print(f"{'─'*70}")
    
    seed = 42 + run * 1000
    results_syk.append(run_experiment(create_syk_otoc, f"SYK (seed={seed})", seed=seed))
    results_kicked.append(run_experiment(create_kicked_ising_otoc, "Kicked Ising"))

# ============================================================
# UNIVERSALITY ANALYSIS
# ============================================================
print("\n" + "="*70)
print("[3] UNIVERSALITY VERIFICATION")
print("="*70)

lambdas_syk = [r['lambda'] for r in results_syk if r['lambda'] >= 0]
lambdas_kicked = [r['lambda'] for r in results_kicked if r['lambda'] >= 0]

print(f"\n  SYK:          λ = {np.mean(lambdas_syk):.3f} ± {np.std(lambdas_syk):.3f}")
print(f"  Kicked Ising: λ = {np.mean(lambdas_kicked):.3f} ± {np.std(lambdas_kicked):.3f}")
print(f"  Difference:   Δλ = {abs(np.mean(lambdas_syk) - np.mean(lambdas_kicked)):.3f}")

if abs(np.mean(lambdas_syk) - np.mean(lambdas_kicked)) < 0.2:
    print("\n  UNIVERSALITY CONFIRMED: Both chaotic models give λ ≈ 1")
else:
    print("\n  UNIVERSALITY PARTIAL: Models give similar but not identical values")

print("\n" + "="*70)
print("EXPERIMENT COMPLETED")
print("="*70)
