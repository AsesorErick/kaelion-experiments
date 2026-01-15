# IBM Quantum OTOC Experiments

## Complete Verification of Kaelion Parameter λ

**Date:** January 14-15, 2026  
**Backends:** ibm_torino, ibm_fez, ibm_marrakesh  
**Status:** ✅ COMPLETED - All three regimes verified

---

## Final Results

| Circuit | λ | α | Confidence |
|---------|---|---|------------|
| **Integrable** | 0.000 ± 0.000 | -0.500 ± 0.000 | ✅ High |
| **Intermediate** | 0.111 ± 0.010 | -0.611 ± 0.010 | ✅ High |
| **Chaotic (Kicked Ising)** | 1.000 ± 0.000 | -1.500 ± 0.000 | ✅ High |

**Kaelion Formula:** α(λ) = -0.5 - λ ✅ **VERIFIED**

---

## Experiments Performed

| Code | Description | Result |
|------|-------------|--------|
| code1 | Ideal simulator comparison | Hardware matches within 5% |
| code2 | Multi-backend (3 QPUs) | Consistent across all |
| code3 | 5 repetitions | Statistical error bars |
| code4 | ZNE error mitigation | Confirms results |
| code5 | Variability investigation | Identified seed dependence |
| code6 | Kicked Ising circuit | 100% stable (solution) |

---

## Key Finding: Kicked Ising vs Random

| Circuit | Stability | Error |
|---------|-----------|-------|
| Random rotations | Variable | ~50% |
| **Kicked Ising** | **Stable** | **0%** |

The Kicked Ising model (J=0.9, h=0.7) provides guaranteed chaos, unlike random rotations.

---

## Files

```
ibm_quantum_otoc/
├── README.md                          # This file
├── code/
│   ├── otoc_v1_basic.py              # Original (has seed bug)
│   ├── otoc_v2_calibrated.py         # Calibrated version
│   ├── generate_figures.py           # Figure generation
│   ├── code1_simulador_ideal.py      # Ideal simulator
│   ├── code2_multi_backend.py        # Multi-QPU test
│   ├── code3_repeticiones.py         # Statistical runs
│   ├── code4_zne.py                  # Error mitigation
│   ├── code5_investigar_variabilidad.py  # Diagnosis
│   └── code6_kicked_ising.py         # RECOMMENDED
├── data/
│   ├── run1_20260114.json
│   ├── run2_20260114.json
│   ├── run3_v21_20260114.json
│   ├── all_experiments_data.json
│   └── results_kicked_ising.json
└── paper/
    ├── paper_operational_lambda.md
    └── figures/
        ├── Figure1_OTOC_Decay.png
        ├── Figure2_Lambda_Values.png
        ├── Figure3_Alpha_Lambda.png
        ├── Figure4_Transpiled_Depths.png
        └── Figure5_Reproducibility.png
```

---

## Quick Start

```bash
# Recommended: Use Kicked Ising circuit
# In Google Colab:

!pip install qiskit qiskit-ibm-runtime scipy -q

# Then run code6_kicked_ising.py
```

---

## Citation

```bibtex
@misc{perez_kaelion_otoc_2026,
  author = {Pérez Eugenio, Erick Francisco},
  title = {Experimental Verification of Kaelion Parameter via OTOC},
  year = {2026},
  publisher = {GitHub},
  url = {https://github.com/AsesorErick/kaelion-experiments}
}
```
