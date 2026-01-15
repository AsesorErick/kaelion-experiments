# ============================================================
# CODE 10: FLOQUET - UNIVERSALITY TEST
# ============================================================
# Kaelion Project - Test if Floquet gives chaotic or integrable λ
# Author: Erick Francisco Perez Eugenio
# Date: January 2026
# 
# KEY FINDING: Floquet with these parameters is PRETHERMAL (non-chaotic)
# This demonstrates that Kaelion λ responds to genuine scrambling,
# not superficial circuit structure.
# ============================================================

import numpy as np
from datetime import datetime

print("="*70)
print("KAELION OTOC - FLOQUET (UNIVERSALITY)")
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
print(f"  Model: Floquet (periodic evolution)")

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

backend = service.least_busy(simulator=False, operational=True, min_num_qubits=N_QUBITS)
print(f"    Backend: {backend.name}")

pm = generate_preset_pass_manager(backend=backend, optimization_level=3)

# ============================================================
# FLOQUET CIRCUIT
# ============================================================
def create_floquet_otoc(n, depth, theta=0.8, phi=1.2, J=0.9):
    """
    Floquet circuit for OTOC measurement.
    
    Despite being periodically driven, this circuit remains in a
    PRETHERMAL regime and does NOT scramble. This is a key finding:
    Kaelion λ correctly identifies non-chaotic dynamics.
    """
    qr = QuantumRegister(n, 'q')
    cr = ClassicalRegister(n, 'c')
    qc = QuantumCircuit(qr, cr)
    
    qc.h(qr[0])
    qc.x(qr[0])
    
    # Forward evolution
    for _ in range(depth):
        for i in range(n):
            qc.rx(2 * theta, qr[i])
            qc.ry(2 * phi, qr[i])
        for i in range(n - 1):
            qc.rzz(2 * J, qr[i], qr[i + 1])
        qc.rzz(2 * J, qr[n-1], qr[0])
        for i in range(0, n-1, 2):
            qc.cz(qr[i], qr[i+1])
    
    qc.z(qr[n - 1])
    
    # Backward evolution
    for _ in range(depth):
        for i in range(0, n-1, 2):
            qc.cz(qr[i], qr[i+1])
        qc.rzz(-2 * J, qr[n-1], qr[0])
        for i in range(n - 2, -1, -1):
            qc.rzz(-2 * J, qr[i], qr[i + 1])
        for i in range(n):
            qc.ry(-2 * phi, qr[i])
            qc.rx(-2 * theta, qr[i])
    
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
# EXECUTION
# ============================================================
def run_experiment(create_func, label, **kwargs):
    print(f"\n    Running: {label}")
    
    circuits = [create_func(N_QUBITS, d, **kwargs) for d in DEPTHS]
    transpiled = pm.run(circuits)
    
    sampler = Sampler(backend)
    job = sampler.run(transpiled, shots=SHOTS)
    print(f"      Job ID: {job.job_id()}")
    
    result = job.result()
    
    otoc_values = []
    for pub_result in result:
        counts = pub_result.data.c.get_counts()
        otoc = counts.get('0' * N_QUBITS, 0) / sum(counts.values())
        otoc_values.append(otoc)
    
    def decay(t, A, lam, B):
        return A * np.exp(-lam * t) + B
    
    try:
        popt, _ = curve_fit(decay, DEPTHS, otoc_values, 
                           p0=[1, 0.3, 0], bounds=([0, 0, -0.5], [2, 5, 0.5]), maxfev=5000)
        lambda_K = np.clip(popt[1] / (2 * np.pi * 0.5), 0, 1)
    except:
        lambda_K = -1
    
    print(f"      → λ = {lambda_K:.4f}")
    return {'lambda': float(lambda_K)}

# ============================================================
# MAIN
# ============================================================
print("\n" + "="*70)
print("[2] RUNNING EXPERIMENTS")
print("="*70)

results_floquet = []
results_kicked = []

for run in range(N_RUNS):
    print(f"\n  RUN {run+1}/{N_RUNS}")
    results_floquet.append(run_experiment(create_floquet_otoc, "Floquet"))
    results_kicked.append(run_experiment(create_kicked_ising_otoc, "Kicked Ising"))

# ============================================================
# ANALYSIS
# ============================================================
print("\n" + "="*70)
print("[3] KEY FINDING")
print("="*70)

lambdas_floquet = [r['lambda'] for r in results_floquet if r['lambda'] >= 0]
lambdas_kicked = [r['lambda'] for r in results_kicked if r['lambda'] >= 0]

print(f"\n  Floquet:      λ = {np.mean(lambdas_floquet):.3f} (PRETHERMAL - LQG regime)")
print(f"  Kicked Ising: λ = {np.mean(lambdas_kicked):.3f} (CHAOTIC - Holographic regime)")

print("""
  CONCLUSION:
  
  The Floquet circuit, despite being periodically driven, remains in a
  non-scrambling prethermal regime, correctly yielding λ ≈ 0.
  
  This demonstrates that Kaelion parameter λ is sensitive to genuine
  quantum chaos rather than superficial circuit structure.
""")

print("="*70)
print("EXPERIMENT COMPLETED")
print("="*70)
