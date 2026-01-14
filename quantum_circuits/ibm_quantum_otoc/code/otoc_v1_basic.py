"""
KAELION OTOC v1 - Basic Version
===============================
First experimental code for IBM Quantum.

NOTE: This version has a seed bug - using same seed across all depths
causes chaotic circuits to repeat same random angles, reducing scrambling.

Used in: Run 1, Run 2
Result: Inverted λ values (chaotic appears integrable)

For correct results, use otoc_v2_calibrated.py
"""

import numpy as np
from datetime import datetime

# API_KEY = "YOUR_API_KEY_HERE"

print("="*60)
print("KAELION OTOC EXPERIMENT - IBM QUANTUM")
print("="*60)

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

N_QUBITS = 4
DEPTHS = [2, 5, 8, 12, 16]
SHOTS = 4096

print("\n[1/4] Conectando a IBM Quantum...")
# QiskitRuntimeService.save_account(
#     channel="ibm_quantum_platform",
#     token=API_KEY,
#     overwrite=True
# )
service = QiskitRuntimeService(channel="ibm_quantum_platform")
print("    ✓ Conectado")

backend = service.least_busy(simulator=False, operational=True, min_num_qubits=N_QUBITS)
print(f"    ✓ Backend: {backend.name}")

def create_otoc(n, depth, ctype, seed=42):
    """
    BUG: Using fixed seed=42 for all depths causes random angles
    to be identical across depths, reducing effective chaos.
    """
    np.random.seed(seed)  # BUG: Should be seed + depth * 100
    qr = QuantumRegister(n, 'q')
    cr = ClassicalRegister(n, 'c')
    qc = QuantumCircuit(qr, cr)
    qc.h(qr[0])
    qc.x(qr[0])
    for _ in range(depth):
        if ctype == 'chaotic':
            for i in range(n):
                qc.u(np.random.uniform(0,2*np.pi), np.random.uniform(0,2*np.pi), 0, qr[i])
            for i in range(n-1): qc.cx(qr[i], qr[i+1])
            qc.cx(qr[n-1], qr[0])
        elif ctype == 'integrable':
            for i in range(n): qc.h(qr[i])
            for i in range(n-1): qc.cx(qr[i], qr[i+1])
        else:
            for i in range(n): qc.h(qr[i]); qc.t(qr[i])
            for i in range(n-1): qc.cx(qr[i], qr[i+1])
    qc.z(qr[n-1])
    qc_inv = QuantumCircuit(qr)
    np.random.seed(seed)  # BUG: Same issue here
    for _ in range(depth):
        if ctype == 'chaotic':
            for i in range(n):
                qc_inv.u(np.random.uniform(0,2*np.pi), np.random.uniform(0,2*np.pi), 0, qr[i])
            for i in range(n-1): qc_inv.cx(qr[i], qr[i+1])
            qc_inv.cx(qr[n-1], qr[0])
        elif ctype == 'integrable':
            for i in range(n): qc_inv.h(qr[i])
            for i in range(n-1): qc_inv.cx(qr[i], qr[i+1])
        else:
            for i in range(n): qc_inv.h(qr[i]); qc_inv.t(qr[i])
            for i in range(n-1): qc_inv.cx(qr[i], qr[i+1])
    qc.compose(qc_inv.inverse(), inplace=True)
    qc.x(qr[0])
    qc.measure(qr, cr)
    return qc

print("\n[2/4] Ejecutando circuitos (5-8 min)...")
results_all = {}
for ctype in ['chaotic', 'integrable', 'intermediate']:
    print(f"\n    ▶ {ctype.upper()}")
    circuits = [create_otoc(N_QUBITS, d, ctype) for d in DEPTHS]
    pm = generate_preset_pass_manager(backend=backend, optimization_level=3)
    transpiled = pm.run(circuits)
    sampler = Sampler(backend)
    job = sampler.run(transpiled, shots=SHOTS)
    print(f"      Job: {job.job_id()} - Esperando...")
    result = job.result()
    otoc_values = []
    for i, pub_result in enumerate(result):
        counts = pub_result.data.c.get_counts()
        otoc = counts.get('0'*N_QUBITS, 0) / sum(counts.values())
        otoc_values.append(otoc)
        print(f"      Depth {DEPTHS[i]:2d}: OTOC = {otoc:.4f}")
    results_all[ctype] = {'depths': DEPTHS, 'otoc': otoc_values}

print("\n[3/4] Análisis...")
from scipy.optimize import curve_fit
def decay(t, A, lam, B): return A * np.exp(-lam * t) + B
mss = 2 * np.pi * 0.5

print(f"\n{'Tipo':<15} {'λ_Lyapunov':<12} {'λ_Kaelion':<12} {'α':<10}")
print("-"*50)
for ctype, data in results_all.items():
    try:
        popt, _ = curve_fit(decay, data['depths'], data['otoc'], p0=[1,0.3,0], bounds=([0,0,-0.5],[2,5,0.5]))
        lam_L, lam_K = popt[1], np.clip(popt[1]/mss, 0, 1)
        alpha = -0.5 - lam_K
        print(f"{ctype:<15} {lam_L:<12.4f} {lam_K:<12.4f} {alpha:<10.4f}")
    except: print(f"{ctype:<15} Error fitting")

print("\n" + "="*60)
print("✓ EXPERIMENTO COMPLETADO")
print("="*60)
