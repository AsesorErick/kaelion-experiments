# Kaelion Experiments

**Experimental Protocols for Verifying the Kaelion Correspondence**

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.PENDING.svg)](https://doi.org/10.5281/zenodo.PENDING)

---

## Overview

This repository contains **concrete experimental protocols** for measuring the Kaelion parameter λ.

**Related repositories:**
- [kaelion](https://github.com/AsesorErick/kaelion) - Main model (DOI: 10.5281/zenodo.18238030)
- [kaelion-derivation](https://github.com/AsesorErick/kaelion-derivation) - Theory (DOI: 10.5281/zenodo.18245761)

---

## Experiments

| Experiment | Platform | Status | Priority |
|------------|----------|--------|----------|
| 1. Quantum Circuits | IBM/Google Quantum | ✅ Ready | 🔴 HIGH |
| 2. BEC Analog | Steinhauer/Weinfurtner labs | ✅ Ready | 🔴 HIGH |
| 3. Astrophysical | LIGO/EHT | ⏳ Future | 🟡 MEDIUM |

---

## Experiment 1: Quantum Circuits

**Location:** `quantum_circuits/experiment1_otoc.py`

**Method:** Measure OTOC decay → Extract Lyapunov → Calculate λ

**Prediction:**
- Chaotic circuits: λ ~ 0.8 (holographic)
- Integrable circuits: λ ~ 0.1 (LQG-like)

**Platform:** IBM Quantum, Google Sycamore, IonQ

**Timeline:** Implementable NOW

---

## Experiment 2: BEC Analog Gravity

**Location:** `bec_analog/experiment2_bec.py`

**Method:** Acoustic black hole → Measure correlations → Fit entropy

**Prediction:**
- S = A/4 + α(λ)·log(A)
- α = -0.5 - λ

**Target Labs:**
- Jeff Steinhauer (Technion)
- Silke Weinfurtner (Nottingham)

**Timeline:** Requires collaboration (6-12 months)

---

## Experiment 3: Astrophysical Signatures

**Location:** `astrophysical/experiment3_astro.py`

**Method:** GW ringdown, BH shadow, X-ray spectra

**Challenge:** Effects are very small (~0.1%)

**Timeline:** Requires next-gen instruments (2035+)

---

## Quick Start

```bash
git clone https://github.com/AsesorErick/kaelion-experiments.git
cd kaelion-experiments

# Run quantum circuit protocol
python3 quantum_circuits/experiment1_otoc.py

# Run BEC protocol
python3 bec_analog/experiment2_bec.py

# Run astrophysical analysis
python3 astrophysical/experiment3_astro.py
```

---

## Falsifiability

**Kaelion is FALSIFIED if:**
- Measured λ falls outside [0, 1]
- α ≠ -0.5 - λ within error bars
- Different measurement methods give inconsistent λ

---

## Citation

```bibtex
@software{perez_kaelion_experiments_2026,
  author = {Pérez Eugenio, Erick Francisco},
  title = {Kaelion Experiments: Protocols for Verification},
  year = {2026},
  publisher = {GitHub},
  url = {https://github.com/AsesorErick/kaelion-experiments}
}
```

---

## License

MIT License

---

## Author

Erick Francisco Pérez Eugenio  
January 2026
