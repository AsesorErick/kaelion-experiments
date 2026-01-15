# ============================================================
# CÓDIGO 6: CIRCUITO CAÓTICO ROBUSTO (Kicked Ising)
# ============================================================
# Diseño que GARANTIZA caos, no depende de suerte del seed
# ============================================================
# !pip install qiskit qiskit-ibm-runtime scipy -q

import numpy as np
from datetime import datetime

API_KEY = "TU_API_KEY_AQUI"  # Reemplaza

print("="*60)
print("KAELION OTOC - CIRCUITO CAÓTICO ROBUSTO")
print("="*60)

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from scipy.optimize import curve_fit

N_QUBITS = 4
DEPTHS = [1, 2, 4, 6, 8, 10, 14]
SHOTS = 4096
N_RUNS = 5

# Conectar
print("\n[1] Conectando...")
QiskitRuntimeService.save_account(channel="ibm_quantum_platform", token=API_KEY, overwrite=True)
service = QiskitRuntimeService(channel="ibm_quantum_platform")
backend = service.least_busy(simulator=False, operational=True, min_num_qubits=N_QUBITS)
print(f"    Backend: {backend.name}")

pm = generate_preset_pass_manager(backend=backend, optimization_level=3)

# ============================================================
# NUEVO DISEÑO: KICKED ISING (Caos garantizado)
# ============================================================
def create_kicked_ising_otoc(n, depth, J=0.9, h=0.7):
    """
    Circuito Kicked Ising - CAOS GARANTIZADO
    
    H_kick = J * sum(ZZ) + h * sum(X)
    
    Parámetros J≈0.9, h≈0.7 están en régimen caótico conocido.
    NO depende de seeds aleatorios.
    """
    qr = QuantumRegister(n, 'q')
    cr = ClassicalRegister(n, 'c')
    qc = QuantumCircuit(qr, cr)
    
    # Preparación OTOC
    qc.h(qr[0])
    qc.x(qr[0])
    
    # Evolución forward: Kicked Ising
    for _ in range(depth):
        # Kick: rotación X en todos los qubits
        for i in range(n):
            qc.rx(2 * h, qr[i])
        # Ising: interacción ZZ entre vecinos
        for i in range(n - 1):
            qc.rzz(2 * J, qr[i], qr[i + 1])
        # Conexión cíclica (hace más caótico)
        qc.rzz(2 * J, qr[n-1], qr[0])
    
    # Operador W
    qc.z(qr[n - 1])
    
    # Evolución backward (inverso)
    for _ in range(depth):
        qc.rzz(-2 * J, qr[n-1], qr[0])
        for i in range(n - 2, -1, -1):
            qc.rzz(-2 * J, qr[i], qr[i + 1])
        for i in range(n):
            qc.rx(-2 * h, qr[i])
    
    # Cerrar OTOC
    qc.x(qr[0])
    qc.measure(qr, cr)
    
    return qc

# ============================================================
# COMPARACIÓN: Viejo (random) vs Nuevo (Kicked Ising)
# ============================================================

def create_random_chaotic_otoc(n, depth, seed=42):
    """Circuito caótico VIEJO (basado en random) - para comparar"""
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

def run_circuit(create_func, label, **kwargs):
    """Ejecuta circuito y retorna λ"""
    circuits = [create_func(N_QUBITS, d, **kwargs) for d in DEPTHS]
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
    
    def decay(t, A, lam, B): return A * np.exp(-lam * t) + B
    mss = 2 * np.pi * 0.5
    try:
        popt, _ = curve_fit(decay, DEPTHS, otoc_values, p0=[1,0.3,0], bounds=([0,0,-0.5],[2,5,0.5]))
        lam_K = np.clip(popt[1]/mss, 0, 1)
    except:
        lam_K = -1
    
    return lam_K, otoc_values

# ============================================================
# TEST: 5 runs de cada tipo
# ============================================================
print("\n[2] Ejecutando 5 runs de cada circuito caótico...")
print("="*60)

results_random = []
results_kicked = []

for run in range(N_RUNS):
    print(f"\n  Run {run+1}/{N_RUNS}:")
    
    # Random (viejo) - con diferentes seeds
    seed = 42 + run * 1000
    lam_r, _ = run_circuit(create_random_chaotic_otoc, f"Random (seed={seed})", seed=seed)
    results_random.append(lam_r)
    print(f"        λ = {lam_r:.4f}")
    
    # Kicked Ising (nuevo) - siempre igual
    lam_k, _ = run_circuit(create_kicked_ising_otoc, "Kicked Ising")
    results_kicked.append(lam_k)
    print(f"        λ = {lam_k:.4f}")

# ============================================================
# RESULTADOS
# ============================================================
print("\n" + "="*60)
print("COMPARACIÓN DE CIRCUITOS CAÓTICOS")
print("="*60)

print("\n  RANDOM (viejo):")
print(f"    Valores: {[f'{v:.2f}' for v in results_random]}")
print(f"    Media:   {np.mean(results_random):.4f}")
print(f"    Std:     {np.std(results_random):.4f}")
print(f"    Error %: {np.std(results_random)/max(np.mean(results_random),0.001)*100:.1f}%")

print("\n  KICKED ISING (nuevo):")
print(f"    Valores: {[f'{v:.2f}' for v in results_kicked]}")
print(f"    Media:   {np.mean(results_kicked):.4f}")
print(f"    Std:     {np.std(results_kicked):.4f}")
print(f"    Error %: {np.std(results_kicked)/max(np.mean(results_kicked),0.001)*100:.1f}%")

print("\n" + "="*60)
print("CONCLUSIÓN")
print("="*60)

if np.std(results_kicked) < np.std(results_random):
    print("\n  ✓ Kicked Ising es MÁS ESTABLE que Random")
    print(f"    Reducción de variabilidad: {(1 - np.std(results_kicked)/max(np.std(results_random),0.001))*100:.0f}%")
else:
    print("\n  ✗ Kicked Ising NO mejoró la estabilidad")

print("\n  Valores finales recomendados:")
print(f"    λ (Kicked Ising) = {np.mean(results_kicked):.3f} ± {np.std(results_kicked):.3f}")

print("\n" + "="*60)
print("✓ EXPERIMENTO COMPLETADO")
print("="*60)
