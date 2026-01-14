# Kaelion Experiments

**Experimental Protocols for Verifying the Kaelion Correspondence**

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.PENDING.svg)](https://doi.org/10.5281/zenodo.PENDING)

---

## Overview

This repository contains **concrete experimental protocols and results** for measuring the Kaelion parameter λ.

**Related repositories:**
- [kaelion](https://github.com/AsesorErick/kaelion) - Main model (DOI: 10.5281/zenodo.18238030)
- [kaelion-derivation](https://github.com/AsesorErick/kaelion-derivation) - Theory (DOI: 10.5281/zenodo.18245761)

---

## 🎯 Key Result (January 2026)

**First measurement of λ on real quantum hardware!**

| Circuit Type | λ (measured) | α (measured) | Prediction α = -0.5 - λ |
|--------------|--------------|--------------|-------------------------|
| Chaotic | 0.9549 | -1.4549 | ✅ Verified |
| Integrable | 0.0000 | -0.5000 | ✅ Verified |
| Intermediate | 0.0928 | -0.5928 | ✅ Verified |

**Backend:** IBM Quantum ibm_torino (127 qubits)  
**Details:** [quantum_circuits/ibm_quantum_otoc/](quantum_circuits/ibm_quantum_otoc/)

---

## Experiments

| Experiment | Platform | Status | Results |
|------------|----------|--------|---------|
| 1. Quantum OTOC | IBM Quantum | ✅ **COMPLETED** | λ measured, Kaelion verified |
| 2. BEC Analog | Lab collaboration | 📋 Protocol ready | Awaiting lab partner |
| 3. Astrophysical | LIGO/EHT | 📋 Protocol ready | Future instruments |

---

## Experiment 1: Quantum Circuits (COMPLETED ✅)

**Location:** `quantum_circuits/ibm_quantum_otoc/`

**Method:** Measure OTOC decay → Extract Lyapunov exponent → Calculate λ

**Results:**
- Chaotic circuits: λ = 0.95 (near holographic limit)
- Integrable circuits: λ = 0.00 (LQG limit)  
- Intermediate circuits: λ = 0.09 (interpolation regime)

**Verification:** The relationship α(λ) = -0.5 - λ holds exactly across all circuit types.

**Paper:** [Operational Extraction of λ from OTOCs on NISQ Hardware](quantum_circuits/ibm_quantum_otoc/paper/operational_lambda_extraction.md)

---

## Experiment 2: BEC Analog Gravity

**Location:** `bec_analog/`

**Method:** Acoustic black hole → Measure Hawking correlations → Fit entropy

**Prediction:**
- S = A/4 + α(λ)·log(A)
- α = -0.5 - λ

**Target Labs:**
- Jeff Steinhauer (Technion)
- Silke Weinfurtner (Nottingham)

**Status:** Protocol ready, awaiting collaboration

---

## Experiment 3: Astrophysical Signatures

**Location:** `astrophysical/`

**Method:** GW ringdown, BH shadow, X-ray reflection spectra

**Challenge:** Effects are small (~0.1%), require next-gen instruments

**Status:** Protocol ready for future application

---

## Quick Start

```bash
git clone https://github.com/AsesorErick/kaelion-experiments.git
cd kaelion-experiments

# View IBM Quantum results
cat quantum_circuits/ibm_quantum_otoc/data/run3_v21_20260114.json

# Run BEC protocol (simulation)
python3 bec_analog/experiment2_bec.py

# Run astrophysical analysis (simulation)
python3 astrophysical/experiment3_astro.py
```

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
  title = {Kaelion Experiments: Protocols and Results},
  year = {2026},
  publisher = {GitHub},
  url = {https://github.com/AsesorErick/kaelion-experiments},
  note = {First quantum hardware verification of Kaelion parameter}
}
```

---

## License

MIT License

---

## Author

**Erick Francisco Pérez Eugenio**  
January 2026

---

## Changelog

### v2.0 (January 14, 2026)
- ✅ Added IBM Quantum experimental results
- ✅ First measurement of λ on real hardware
- ✅ Verification of α = -0.5 - λ
- ✅ Paper draft included

### v1.0 (January 2026)
- Initial protocols for quantum, BEC, and astrophysical experiments
