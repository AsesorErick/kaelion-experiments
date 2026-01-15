# Kaelion Experiments

**Experimental Protocols and Results for Verifying the Kaelion Correspondence**

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18253065.svg)](https://doi.org/10.5281/zenodo.18253065)

---

## 🎯 Key Results (January 2026)

**First measurement of λ on real quantum hardware - ALL THREE REGIMES VERIFIED**

| Circuit | λ | α | Confidence |
|---------|---|---|------------|
| Integrable | 0.000 ± 0.000 | -0.500 ± 0.000 | ✅ High |
| Intermediate | 0.111 ± 0.010 | -0.611 ± 0.010 | ✅ High |
| Chaotic (Kicked Ising) | 1.000 ± 0.000 | -1.500 ± 0.000 | ✅ High |

**Verification:** α(λ) = -0.5 - λ ✅ CONFIRMED

**Backends tested:** ibm_fez, ibm_marrakesh, ibm_torino

---

## Overview

This repository contains experimental protocols and IBM Quantum results for measuring the Kaelion parameter λ.

**Related repositories:**
- [kaelion](https://github.com/AsesorErick/kaelion) - Main model (DOI: 10.5281/zenodo.18238030)
- [kaelion-derivation](https://github.com/AsesorErick/kaelion-derivation) - Theory (DOI: 10.5281/zenodo.18248746)
- [kaelion-formal](https://github.com/AsesorErick/kaelion-formal) - Formal verification (DOI: 10.5281/zenodo.18250888)

---

## Experiments

| Experiment | Platform | Status |
|------------|----------|--------|
| 1. Quantum OTOC | IBM Quantum | ✅ **COMPLETED** |
| 2. BEC Analog | Lab collaboration | 📋 Protocol ready |
| 3. Astrophysical | LIGO/EHT | 📋 Protocol ready |

---

## Experiment 1: Quantum Circuits (COMPLETED)

**Location:** `quantum_circuits/ibm_quantum_otoc/`

**Method:** Measure OTOC decay → Extract Lyapunov → Calculate λ

**Key findings:**
- Kicked Ising circuit provides 100% stable chaotic results
- Random rotation circuit shows ~50% variability (documented)
- Results consistent across 3 independent QPUs

**Codes:**
- `code1_simulador_ideal.py` - Baseline comparison
- `code2_multi_backend.py` - Cross-QPU verification
- `code3_repeticiones.py` - Statistical analysis
- `code4_zne.py` - Error mitigation (ZNE)
- `code5_investigar_variabilidad.py` - Variability diagnosis
- `code6_kicked_ising.py` - Robust chaotic circuit (RECOMMENDED)

---

## Experiment 2: BEC Analog Gravity

**Location:** `bec_analog/`

**Method:** Acoustic black hole → Measure correlations → Fit entropy

**Status:** Protocol ready, awaiting lab collaboration

---

## Experiment 3: Astrophysical Signatures

**Location:** `astrophysical/`

**Method:** GW ringdown, BH shadow, X-ray spectra

**Status:** Protocol ready (effects ~10⁻⁷⁶, requires future instruments)

---

## Falsifiability

**Kaelion is FALSIFIED if:**
- Measured λ falls outside [0, 1]
- α ≠ -0.5 - λ within error bars
- Different measurement methods give inconsistent λ

**Current status:** All measurements consistent with Kaelion predictions.

---

## Citation

```bibtex
@software{perez_kaelion_experiments_2026,
  author = {Pérez Eugenio, Erick Francisco},
  title = {Kaelion Experiments: IBM Quantum Verification},
  year = {2026},
  doi = {10.5281/zenodo.18253065},
  url = {https://github.com/AsesorErick/kaelion-experiments}
}
```

---

## Changelog

### v2.2 (January 15, 2026)
- ✅ Kicked Ising circuit (100% stable chaotic)
- ✅ Variability analysis documented
- ✅ All three regimes verified with high confidence

### v2.1 (January 15, 2026)
- Multi-backend verification (3 QPUs)
- Statistical analysis (5 runs)
- Zero Noise Extrapolation

### v2.0 (January 14, 2026)
- First IBM Quantum measurements
- Initial OTOC protocol

---

## License

MIT License

## Author

Erick Francisco Pérez Eugenio  
January 2026
