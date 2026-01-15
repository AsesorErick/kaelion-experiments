# ============================================================
# CÓDIGO 3: MÁS REPETICIONES (Google Colab)
# ============================================================
# 5 runs para calcular media y error estándar
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
print("KAELION OTOC - MÚLTIPLES REPETICIONES")
print("="*60)

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

N_QUBITS = 4
DEPTHS = [1, 2, 4, 6, 8, 10, 14]
SHOTS = 4096
N_RUNS = 5  # Número de repeticiones

# Conectar
print("\n[1] Conectando...")
QiskitRuntimeService.save_account(channel="ibm_quantum_platform", token=API_KEY, overwrite=True)
service = QiskitRuntimeService(channel="ibm_quantum_platform")
backend = service.least_busy(simulator=False, operational=True, min_num_qubits=N_QUBITS)
print(f"    Backend: {backend.name}")

pm = generate_preset_pass_manager(backend=backend, optimization_level=3)

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

# Ejecutar múltiples runs
all_lambdas = {'chaotic': [], 'integrable': [], 'intermediate': []}

from scipy.optimize import curve_fit
def decay(t, A, lam, B): return A * np.exp(-lam * t) + B
mss = 2 * np.pi * 0.5

for run in range(N_RUNS):
    print(f"\n[Run {run+1}/{N_RUNS}]")
    
    for ctype in ['chaotic', 'integrable', 'intermediate']:
        circuits = [create_otoc(N_QUBITS, d, ctype, seed=42+run*1000) for d in DEPTHS]
        transpiled = pm.run(circuits)
        
        sampler = Sampler(backend)
        job = sampler.run(transpiled, shots=SHOTS)
        print(f"  {ctype}: Job {job.job_id()}")
        result = job.result()
        
        otoc_values = []
        for pub_result in result:
            counts = pub_result.data.c.get_counts()
            otoc = counts.get('0'*N_QUBITS, 0) / sum(counts.values())
            otoc_values.append(otoc)
        
        try:
            popt, _ = curve_fit(decay, DEPTHS, otoc_values, p0=[1,0.3,0], bounds=([0,0,-0.5],[2,5,0.5]))
            lam_K = np.clip(popt[1]/mss, 0, 1)
            all_lambdas[ctype].append(lam_K)
            print(f"    λ = {lam_K:.4f}")
        except:
            print(f"    Error fitting")

# Estadísticas
print("\n" + "="*60)
print("ESTADÍSTICAS ({} RUNS)".format(N_RUNS))
print("="*60)

print(f"\n{'Tipo':<15} {'λ media':<12} {'λ std':<12} {'Error %':<10}")
print("-"*50)

final_results = {}
for ctype in ['chaotic', 'integrable', 'intermediate']:
    vals = np.array(all_lambdas[ctype])
    mean = np.mean(vals)
    std = np.std(vals)
    err_pct = (std/mean*100) if mean > 0 else 0
    final_results[ctype] = {'mean': mean, 'std': std}
    print(f"{ctype:<15} {mean:<12.4f} {std:<12.4f} {err_pct:<10.1f}%")

# Verificación Kaelion
print("\n" + "="*60)
print("VERIFICACIÓN KAELION (con barras de error)")
print("="*60)
print(f"\n{'Tipo':<15} {'λ':<15} {'α':<15}")
print("-"*45)
for ctype, data in final_results.items():
    lam = data['mean']
    lam_err = data['std']
    alpha = -0.5 - lam
    alpha_err = lam_err
    print(f"{ctype:<15} {lam:.3f} ± {lam_err:.3f}   {alpha:.3f} ± {alpha_err:.3f}")

print("\n✓ COMPLETADO")
