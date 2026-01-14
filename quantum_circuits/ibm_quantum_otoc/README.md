# IBM Quantum OTOC Experiments

## First Measurement of λ via OTOC Decay on NISQ Hardware

**Date:** January 14, 2026  
**Backend:** ibm_torino (127 qubits)  
**Status:** ✅ COMPLETED - Data collected

---

## Results Summary

| Circuit Type | λ (Kaelion) | α | Verification |
|--------------|-------------|---|--------------|
| Chaotic | 0.9549 | -1.4549 | ✅ α = -0.5 - λ |
| Integrable | 0.0000 | -0.5000 | ✅ α = -0.5 - λ |
| Intermediate | 0.0928 | -0.5928 | ✅ α = -0.5 - λ |

**Key finding:** The relationship α(λ) = -0.5 - λ holds exactly across all circuit types.

---

## Files

```
ibm_quantum_otoc/
├── README.md                    # This file
├── paper/
│   ├── operational_lambda_extraction.md   # Paper draft
│   └── figures/
│       ├── Figure1_OTOC_Decay.png
│       ├── Figure2_Lambda_Values.png
│       ├── Figure3_Alpha_Lambda.png
│       ├── Figure4_Transpiled_Depths.png
│       └── Figure5_Reproducibility.png
├── code/
│   ├── otoc_v1_basic.py         # First version (runs 1-2)
│   ├── otoc_v2_calibrated.py    # Calibrated version (run 3)
│   └── generate_figures.py      # Figure generation
└── data/
    ├── run1_20260114.json
    ├── run2_20260114.json
    └── run3_v21_20260114.json
```

---

## IBM Quantum Job IDs (for reproducibility)

### Run 1 (v1)
- Chaotic: `d5k1nojtlojc73f68olg`
- Integrable: `d5k1nrjtlojc73f68oog`
- Intermediate: `d5k1nucjt3vs73drtgn0`

### Run 2 (v1)
- Chaotic: `d5k1t3jtlojc73f68tog`
- Integrable: `d5k1t6kjt3vs73drtm70`
- Intermediate: `d5k1t9n853es738dbcf0`

### Run 3 (v2.1 - Calibrated)
- Calibration: `d5k1vtbtlojc73f690lg`
- Chaotic: `d5k20bqvcahs73a1eu5g`
- Integrable: `d5k20favcahs73a1eua0`
- Intermediate: `d5k20ikjt3vs73drtq40`

---

## Quick Start

```bash
# Install dependencies
pip install qiskit qiskit-ibm-runtime scipy matplotlib

# Run experiment (requires IBM Quantum API key)
python code/otoc_v2_calibrated.py

# Generate figures
python code/generate_figures.py
```

---

## Citation

```bibtex
@misc{perez_kaelion_otoc_2026,
  author = {Pérez Eugenio, Erick Francisco},
  title = {Operational Extraction of λ from OTOC Decay on NISQ Hardware},
  year = {2026},
  publisher = {GitHub},
  url = {https://github.com/AsesorErick/kaelion-experiments/tree/main/quantum_circuits/ibm_quantum_otoc}
}
```

---

## Related

- [Main Kaelion Model](https://github.com/AsesorErick/kaelion) - DOI: 10.5281/zenodo.18238030
- [Kaelion Derivation](https://github.com/AsesorErick/kaelion-derivation) - DOI: 10.5281/zenodo.18245761
