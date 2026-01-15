# ============================================================
# CÓDIGO 2: MULTI-BACKEND (Google Colab)
# ============================================================
# Prueba en diferentes QPUs para verificar universalidad
# ============================================================
# Celda 1: Instalar
# !pip install qiskit qiskit-ibm-runtime scipy -q

# ============================================================
# Celda 2: Ejecutar
# ============================================================
import numpy as np
from datetime import datetime

API_KEY = "0pQiHdG9N4OigDR0Wi3FKYqx0a6BF2BDJ6NyoR-gd2Fz"

print("="*60)
print("KAELION OTOC - MULTI-BACKEND")
print("="*60)

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

N_QUBITS = 4
DEPTHS = [1, 2, 4, 6, 8, 10, 14]
SHOTS = 4096

# Conectar
print("\n[1] Conectando a IBM Quantum...")
QiskitRuntimeService.save_account(channel="ibm_quantum_platform", token=API_KEY, overwrite=True)
service = QiskitRuntimeService(channel="ibm_quantum_platform")

# Listar backends disponibles
backends_available = service.backends(simulator=False, operational=True, min_num_qubits=N_QUBITS)
print(f"    Backends disponibles: {[b.name for b in backends_available]}")

# Seleccionar hasta 3 backends diferentes
TARGET_BACKENDS = []
for b in backends_available:
    if len(TARGET_BACKENDS) < 3:
        TARGET_BACKENDS.append(b.name)
print(f"    Usando: {TARGET_BACKENDS}")

def create_otoc(n, depth, ctype, seed=42):
    np.random.seed(seed + depth * 100)
    qr = QuantumRegister(n, 'q')
    cr = ClassicalRegister(n, 'c')
    qc = QuantumCircuit(qr, cr)
    qc.h(qr[0])
    qc.x(qr[0])
    for d in range(depth):
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
    np.random.seed(seed + depth * 100)
    qc_inv = QuantumCircuit(qr)
    for d in range(depth):
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

# Ejecutar en cada backend
all_results = {}

for backend_name in TARGET_BACKENDS:
    print(f"\n[2] Backend: {backend_name}")
    backend = service.backend(backend_name)
    pm = generate_preset_pass_manager(backend=backend, optimization_level=3)
    
    backend_results = {}
    
    for ctype in ['chaotic', 'integrable', 'intermediate']:
        print(f"    ▶ {ctype}")
        circuits = [create_otoc(N_QUBITS, d, ctype) for d in DEPTHS]
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
        
        backend_results[ctype] = otoc_values
        print(f"      OTOC: {[f'{v:.3f}' for v in otoc_values]}")
    
    all_results[backend_name] = backend_results

# Análisis
from scipy.optimize import curve_fit
def decay(t, A, lam, B): return A * np.exp(-lam * t) + B
mss = 2 * np.pi * 0.5

print("\n" + "="*60)
print("RESULTADOS POR BACKEND")
print("="*60)

print(f"\n{'Backend':<20} {'Chaotic λ':<12} {'Integrable λ':<14} {'Interm λ':<12}")
print("-"*60)

for backend_name, results in all_results.items():
    lambdas = []
    for ctype in ['chaotic', 'integrable', 'intermediate']:
        try:
            popt, _ = curve_fit(decay, DEPTHS, results[ctype], p0=[1,0.3,0], bounds=([0,0,-0.5],[2,5,0.5]))
            lam_K = np.clip(popt[1]/mss, 0, 1)
            lambdas.append(lam_K)
        except:
            lambdas.append(-1)
    print(f"{backend_name:<20} {lambdas[0]:<12.4f} {lambdas[1]:<14.4f} {lambdas[2]:<12.4f}")

print("\n" + "="*60)
print("✓ MULTI-BACKEND COMPLETADO")
print("="*60)
