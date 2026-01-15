# ============================================================
# CÓDIGO 1: SIMULADOR IDEAL (Google Colab)
# ============================================================
# Celda 1: Instalar
# ============================================================
# !pip install qiskit qiskit-aer scipy -q
# print("✓ Instalado")

# ============================================================
# Celda 2: Ejecutar simulación
# ============================================================
import numpy as np
from datetime import datetime

print("="*60)
print("KAELION OTOC - SIMULADOR IDEAL (Sin ruido)")
print("="*60)

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator

N_QUBITS = 4
DEPTHS = [1, 2, 4, 6, 8, 10, 14]
SHOTS = 100000

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

print("\nEjecutando simulador ideal...")
simulator = AerSimulator(method='statevector')
results_ideal = {}

for ctype in ['chaotic', 'integrable', 'intermediate']:
    print(f"\n  ▶ {ctype.upper()}")
    otoc_values = []
    for d in DEPTHS:
        qc = create_otoc(N_QUBITS, d, ctype)
        job = simulator.run(qc, shots=SHOTS)
        counts = job.result().get_counts()
        otoc = counts.get('0'*N_QUBITS, 0) / SHOTS
        otoc_values.append(otoc)
        print(f"    Depth {d:2d}: OTOC = {otoc:.6f}")
    results_ideal[ctype] = {'depths': DEPTHS, 'otoc': otoc_values}

# Análisis
from scipy.optimize import curve_fit
def decay(t, A, lam, B): return A * np.exp(-lam * t) + B
mss = 2 * np.pi * 0.5

print("\n" + "="*60)
print("RESULTADOS SIMULADOR IDEAL")
print("="*60)
print(f"\n{'Tipo':<15} {'λ_Kaelion':<12} {'α':<10}")
print("-"*40)

analysis_ideal = {}
for ctype, data in results_ideal.items():
    try:
        popt, _ = curve_fit(decay, data['depths'], data['otoc'], p0=[1,0.3,0], bounds=([0,0,-0.5],[2,5,0.5]))
        lam_K = np.clip(popt[1]/mss, 0, 1)
        alpha = -0.5 - lam_K
        analysis_ideal[ctype] = {'lambda_K': lam_K, 'alpha': alpha, 'otoc': data['otoc']}
        print(f"{ctype:<15} {lam_K:<12.4f} {alpha:<10.4f}")
    except: print(f"{ctype:<15} Error fitting")

# Comparación con hardware
print("\n" + "="*60)
print("COMPARACIÓN: IDEAL vs HARDWARE (ibm_torino)")
print("="*60)
hw = {'chaotic': 0.9549, 'integrable': 0.0000, 'intermediate': 0.0928}
print(f"\n{'Tipo':<15} {'λ ideal':<12} {'λ hardware':<12} {'Δλ':<10}")
print("-"*50)
for ctype in ['chaotic', 'integrable', 'intermediate']:
    li = analysis_ideal[ctype]['lambda_K']
    lh = hw[ctype]
    print(f"{ctype:<15} {li:<12.4f} {lh:<12.4f} {abs(li-lh):<10.4f}")

print("\n✓ SIMULACIÓN COMPLETADA")
