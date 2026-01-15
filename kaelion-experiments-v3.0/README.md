# Kaelion Experiments v3.0

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18253868.svg)](https://doi.org/10.5281/zenodo.18253868)

Experimental verification of the Kaelion parameter λ on IBM Quantum hardware.

## Author

**Erick Francisco Perez Eugenio**  
Independent Researcher

## Core Result

The Kaelion formula **α(λ) = -0.5 - λ** has been verified experimentally:

| Model | λ | α | Regime |
|-------|---|---|--------|
| Kicked Ising (4q) | 1.000 ± 0.000 | -1.500 | Holographic |
| SYK (4q) | 0.890 ± 0.221 | -1.390 | Holographic |
| Floquet (4q) | 0.004 ± 0.000 | -0.504 | LQG (prethermal) |
| Integrable (4q) | 0.000 ± 0.000 | -0.500 | LQG |

## Key Finding

The Floquet circuit, despite being periodically driven, remains in a non-scrambling prethermal regime, correctly yielding λ ≈ 0. This demonstrates that **Kaelion parameter λ is sensitive to genuine quantum chaos rather than superficial circuit structure.**

## Scaling Analysis (NISQ Limits)

| Qubits | λ | Max Depth | Status |
|--------|---|-----------|--------|
| 4 | 1.000 | ~200 | Ideal |
| 8 | 0.172 | ~2400 | Hardware limited |
| 12 | 0.294 | ~2375 | Hardware limited |

## Repository Structure

```
kaelion-experiments/
├── quantum_circuits/
│   └── ibm_quantum_otoc/
│       ├── code/
│       │   ├── code6_kicked_ising.py
│       │   ├── code7_kicked_ising_8qubits.py
│       │   ├── code8_kicked_ising_12qubits.py
│       │   ├── code9_syk_simplificado.py
│       │   ├── code10_floquet.py
│       │   └── code11_depths_reducidos_8q.py
│       ├── data/
│       │   └── all_experiments_data_FINAL.json
│       └── paper/
│           └── paper_operational_lambda.md
├── bec_analog/
│   └── experiment2_bec.py (protocol ready, not executed)
├── astrophysical/
│   └── experiment3_astro.py (future protocol)
├── LICENSE
└── README.md
```

## Hardware

- **Provider:** IBM Quantum
- **Backends:** ibm_fez (primary), ibm_torino, ibm_marrakesh
- **Shots:** 4096 per circuit
- **Dates:** January 14-15, 2026

## Related Repositories

| Repository | DOI | Description |
|------------|-----|-------------|
| [kaelion](https://github.com/AsesorErick/kaelion) | [10.5281/zenodo.18238030](https://doi.org/10.5281/zenodo.18238030) | Core framework |
| [kaelion-derivation](https://github.com/AsesorErick/kaelion-derivation) | [10.5281/zenodo.18248746](https://doi.org/10.5281/zenodo.18248746) | Theoretical derivation |
| [kaelion-formal](https://github.com/AsesorErick/kaelion-formal) | [10.5281/zenodo.18250888](https://doi.org/10.5281/zenodo.18250888) | Formal verification |

## Installation

```bash
pip install qiskit qiskit-ibm-runtime scipy numpy matplotlib
```

## Usage

```python
# Replace with your IBM Quantum API key
API_KEY = "your_api_key_here"

# Run any code file
python code6_kicked_ising.py
```

## Citation

```bibtex
@software{perez_eugenio_2026_kaelion_experiments,
  author       = {Perez Eugenio, Erick Francisco},
  title        = {Kaelion Experiments v3.0},
  month        = jan,
  year         = 2026,
  publisher    = {Zenodo},
  version      = {v3.0},
  doi          = {10.5281/zenodo.18253868},
  url          = {https://doi.org/10.5281/zenodo.18253868}
}
```

## License

MIT License - see [LICENSE](LICENSE)
