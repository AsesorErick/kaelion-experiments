# ============================================================
# CÓDIGO 5: INVESTIGAR VARIABILIDAD CHAOTIC
# ============================================================
# Diagnóstico: ¿Es el seed o es el hardware?
# ============================================================
# !pip install qiskit qiskit-ibm-runtime scipy -q

import numpy as np
from datetime import datetime

API_KEY = "TU_API_KEY_AQUI"  # Reemplaza con tu key

print("="*60)
print("INVESTIGACIÓN: VARIABILIDAD EN CHAOTIC")
print("="*60)

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from scipy.optimize import curve_fit

N_QUBITS = 4
DEPTHS = [1, 2, 4, 6, 8, 10, 14]
SHOTS = 4096

# Conectar
print("\n[1] Conectando...")
QiskitRuntimeService.save_account(channel="ibm_quantum_platform", token=API_KEY, overwrite=True)
service = QiskitRuntimeService(channel="ibm_quantum_platform")
backend = service.backend("ibm_fez")  # Mismo backend que runs originales
print(f"    Backend: {backend.name}")

pm = generate_preset_pass_manager(backend=backend, optimization_level=3)

def create_otoc_chaotic(n, depth, seed):
    """Circuito caótico con seed específico"""
    np.random.seed(seed + depth * 100)
    qr = QuantumRegister(n, 'q')
    cr = ClassicalRegister(n, 'c')
    qc = QuantumCircuit(qr, cr)
    qc.h(qr[0])
    qc.x(qr[0])
    for d in range(depth):
        for i in range(n):
            qc.u(np.random.uniform(0,2*np.pi), np.random.uniform(0,2*np.pi), 0, qr[i])
        for i in range(n-1): qc.cx(qr[i], qr[i+1])
        qc.cx(qr[n-1], qr[0])
    qc.z(qr[n-1])
    np.random.seed(seed + depth * 100)
    qc_inv = QuantumCircuit(qr)
    for d in range(depth):
        for i in range(n):
            qc_inv.u(np.random.uniform(0,2*np.pi), np.random.uniform(0,2*np.pi), 0, qr[i])
        for i in range(n-1): qc_inv.cx(qr[i], qr[i+1])
        qc_inv.cx(qr[n-1], qr[0])
    qc.compose(qc_inv.inverse(), inplace=True)
    qc.x(qr[0])
    qc.measure(qr, cr)
    return qc

def run_and_extract_lambda(seed, label):
    """Ejecuta circuito y extrae λ"""
    circuits = [create_otoc_chaotic(N_QUBITS, d, seed) for d in DEPTHS]
    transpiled = pm.run(circuits)
    sampler = Sampler(backend)
    job = sampler.run(transpiled, shots=SHOTS)
    print(f"    {label}: Job {job.job_id()}")
    result = job.result()
    
    otoc_values = []
    for pub_result in result:
        counts = pub_result.data.c.get_counts()
        otoc = counts.get('0'*N_QUBITS, 0) / sum(counts.values())
        otoc_values.append(otoc)
    
    # Fit
    def decay(t, A, lam, B): return A * np.exp(-lam * t) + B
    mss = 2 * np.pi * 0.5
    try:
        popt, _ = curve_fit(decay, DEPTHS, otoc_values, p0=[1,0.3,0], bounds=([0,0,-0.5],[2,5,0.5]))
        lam_K = np.clip(popt[1]/mss, 0, 1)
    except:
        lam_K = -1
    
    return lam_K, otoc_values

# ============================================================
# TEST 1: Repetir seeds problemáticos (4042, 5042)
# ============================================================
print("\n[2] TEST 1: Repetir seeds problemáticos")
print("-"*50)

seed_4 = 42 + 4*1000  # 4042
seed_5 = 42 + 5*1000  # 5042

lam_4_repeat, otoc_4 = run_and_extract_lambda(seed_4, "Seed 4042 (repeat)")
print(f"        λ = {lam_4_repeat:.4f}")

lam_5_repeat, otoc_5 = run_and_extract_lambda(seed_5, "Seed 5042 (repeat)")
print(f"        λ = {lam_5_repeat:.4f}")

print("\n    Comparación con originales:")
print(f"    Seed 4042: Original λ=0.0138, Repeat λ={lam_4_repeat:.4f}")
print(f"    Seed 5042: Original λ=0.0025, Repeat λ={lam_5_repeat:.4f}")

# ============================================================
# TEST 2: Seeds "buenos" (1042, 2042, 3042) - verificar
# ============================================================
print("\n[3] TEST 2: Verificar seeds buenos")
print("-"*50)

for run_num in [1, 2, 3]:
    seed = 42 + run_num*1000
    lam, _ = run_and_extract_lambda(seed, f"Seed {seed}")
    print(f"        λ = {lam:.4f} (original: 1.0000)")

# ============================================================
# TEST 3: Seed fijo, múltiples runs (solo variabilidad hardware)
# ============================================================
print("\n[4] TEST 3: Mismo seed (42), 3 runs (solo hardware)")
print("-"*50)

fixed_seed_results = []
for i in range(3):
    lam, _ = run_and_extract_lambda(42, f"Run {i+1} (seed=42)")
    fixed_seed_results.append(lam)
    print(f"        λ = {lam:.4f}")

print(f"\n    Media: {np.mean(fixed_seed_results):.4f}")
print(f"    Std:   {np.std(fixed_seed_results):.4f}")

# ============================================================
# DIAGNÓSTICO
# ============================================================
print("\n" + "="*60)
print("DIAGNÓSTICO")
print("="*60)

print("\n¿Es problema del SEED?")
if lam_4_repeat < 0.5 and lam_5_repeat < 0.5:
    print("  → SÍ: Seeds 4042 y 5042 consistentemente dan λ bajo")
    print("  → Solución: Evitar estos seeds o rediseñar circuito")
else:
    print("  → NO: Los seeds ahora dan valores diferentes")
    print("  → Fue variabilidad del hardware")

print("\n¿Es problema del HARDWARE?")
hw_std = np.std(fixed_seed_results)
if hw_std > 0.1:
    print(f"  → SÍ: Variabilidad hardware alta (std={hw_std:.3f})")
else:
    print(f"  → NO: Hardware estable (std={hw_std:.3f})")

print("\n" + "="*60)
print("✓ INVESTIGACIÓN COMPLETADA")
print("="*60)
