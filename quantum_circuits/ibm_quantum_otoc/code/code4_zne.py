# ============================================================
# CÓDIGO 4: ZNE - ZERO NOISE EXTRAPOLATION (Google Colab)
# ============================================================
# Mitigación de errores avanzada
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
print("KAELION OTOC - ZERO NOISE EXTRAPOLATION")
print("="*60)

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

N_QUBITS = 4
DEPTHS = [1, 2, 4, 6, 8, 10, 14]
SHOTS = 4096
NOISE_FACTORS = [1, 2, 3]  # Factores de amplificación de ruido

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

def amplify_noise(qc, factor):
    """
    Amplifica ruido repitiendo puertas CNOT.
    Factor 1 = normal, Factor 2 = doble ruido, etc.
    """
    if factor == 1:
        return qc
    
    qc_amp = QuantumCircuit(qc.num_qubits, qc.num_clbits)
    
    for inst, qargs, cargs in qc.data:
        qc_amp.append(inst, qargs, cargs)
        # Repetir CNOTs para amplificar ruido
        if inst.name == 'cx' and factor > 1:
            for _ in range(factor - 1):
                qc_amp.cx(qargs[0], qargs[1])
                qc_amp.cx(qargs[0], qargs[1])  # Par CNOT = identidad
    
    return qc_amp

def zne_extrapolate(noise_factors, values):
    """
    Extrapolación a ruido cero usando fit lineal.
    """
    coeffs = np.polyfit(noise_factors, values, deg=1)
    return coeffs[1]  # Valor en factor=0

# Ejecutar con diferentes niveles de ruido
print("\n[2] Ejecutando ZNE...")

zne_results = {}

for ctype in ['chaotic', 'integrable', 'intermediate']:
    print(f"\n  ▶ {ctype.upper()}")
    
    otoc_by_factor = {f: [] for f in NOISE_FACTORS}
    
    for noise_factor in NOISE_FACTORS:
        print(f"    Noise factor {noise_factor}x:")
        
        circuits = []
        for d in DEPTHS:
            qc = create_otoc(N_QUBITS, d, ctype)
            qc_amp = amplify_noise(qc, noise_factor)
            circuits.append(qc_amp)
        
        transpiled = pm.run(circuits)
        sampler = Sampler(backend)
        job = sampler.run(transpiled, shots=SHOTS)
        print(f"      Job: {job.job_id()}")
        result = job.result()
        
        for pub_result in result:
            counts = pub_result.data.c.get_counts()
            otoc = counts.get('0'*N_QUBITS, 0) / sum(counts.values())
            otoc_by_factor[noise_factor].append(otoc)
    
    # Extrapolación ZNE para cada depth
    otoc_zne = []
    for i in range(len(DEPTHS)):
        values = [otoc_by_factor[f][i] for f in NOISE_FACTORS]
        zne_val = zne_extrapolate(NOISE_FACTORS, values)
        otoc_zne.append(max(0, min(1, zne_val)))  # Clamp to [0,1]
    
    zne_results[ctype] = {
        'otoc_raw': otoc_by_factor[1],
        'otoc_zne': otoc_zne
    }
    
    print(f"    ZNE OTOC: {[f'{v:.3f}' for v in otoc_zne]}")

# Análisis
from scipy.optimize import curve_fit
def decay(t, A, lam, B): return A * np.exp(-lam * t) + B
mss = 2 * np.pi * 0.5

print("\n" + "="*60)
print("RESULTADOS ZNE")
print("="*60)

print(f"\n{'Tipo':<15} {'λ raw':<12} {'λ ZNE':<12} {'Mejora':<10}")
print("-"*50)

for ctype, data in zne_results.items():
    try:
        popt_raw, _ = curve_fit(decay, DEPTHS, data['otoc_raw'], p0=[1,0.3,0], bounds=([0,0,-0.5],[2,5,0.5]))
        lam_raw = np.clip(popt_raw[1]/mss, 0, 1)
    except:
        lam_raw = -1
    
    try:
        popt_zne, _ = curve_fit(decay, DEPTHS, data['otoc_zne'], p0=[1,0.3,0], bounds=([0,0,-0.5],[2,5,0.5]))
        lam_zne = np.clip(popt_zne[1]/mss, 0, 1)
    except:
        lam_zne = -1
    
    mejora = "✓" if abs(lam_zne - lam_raw) < 0.1 else "~"
    print(f"{ctype:<15} {lam_raw:<12.4f} {lam_zne:<12.4f} {mejora}")

print("\n" + "="*60)
print("✓ ZNE COMPLETADO")
print("="*60)
