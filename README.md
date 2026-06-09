# ML-TightBinding-IIIV

**Machine Learning Prediction of sp³s\* Tight-Binding Parameters for III-V Binary Semiconductors**

[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3%2B-orange.svg)](https://scikit-learn.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **Associated paper:** D. Malkoç and R. Hoşavcı, "Investigation of Machine Learning Models for sp³s\* Tight-Binding Parameter Prediction in III-V Binary Semiconductors," *CAS 2026* (submitted).

---

## Overview

This repository provides a DFT-free, data-driven framework for predicting sp³s\* tight-binding (TB) parameters of nine III-V binary semiconductors directly from experimentally measurable quantities — without requiring first-principles calculations.

**Key idea:** Instead of running costly density functional theory (DFT) or genetic algorithm optimizations for each new material, we train ML models to map macroscopic observables (band gaps, spin-orbit splitting, effective mass, lattice constant) → 16 sp³s\* TB parameters.

### Materials

GaAs · AlAs · InAs · GaP · AlP · InP · GaSb · AlSb · InSb

### Models Compared

| Model | Best Target | MAPE |
|-------|------------|------|
| **SVR** (RBF kernel) | Eg(Γ) | 1.2% (12-feat) |
| **GBR** (Gradient Boosting) | Δso | 0.9% (12-feat) |
| **MLP** (Neural Network) | me* | 4.2% (12-feat) |

---

## Repository Structure

```
ML-TightBinding-IIIV/
│
├── README.md                  # This file
├── requirements.txt           # Python dependencies
├── LICENSE                    # MIT License
│
├── tb_ml_optim.py             # Core module: Hamiltonian, data generation, material definitions
├── comparison_all.py          # Main pipeline: train, evaluate, and compare all 6 models
├── physics_features.py        # 12-feature physics-informed descriptor computation
├── harrison.py                # Harrison universal TB parameter calculator
│
├── data/
│   ├── results_table.csv      # Per-material prediction results (Eg, Δso, me*)
│   └── tb_params_svr.csv      # Predicted TB parameters vs Klimeck reference
│
├── figures/
│   ├── eg_per_material.png    # Eg(Γ) predictions per material (3×3 grid)
│   └── dso_per_material.png   # Δso predictions per material (3×3 grid)
│
└── notebooks/
    └── demo.ipynb             # Quick-start demo notebook
```

---

## Quick Start

### 1. Clone and install

```bash
git clone https://github.com/reyhanhosavci/ML-TightBinding-IIIV.git
cd ML-TightBinding-IIIV
pip install -r requirements.txt
```

### 2. Run the full comparison

```bash
python comparison_all.py
```

This will:
- Generate 4,500 synthetic training samples (9 materials × 500 perturbations at ±4%)
- Train SVR, GBR, and MLP models with both 6-feature and 12-feature input sets
- Evaluate against experimental targets from Vurgaftman et al. (2001)
- Output results tables and comparison figures

### 3. Explore interactively

```bash
jupyter notebook notebooks/demo.ipynb
```

---

## Method

### Training Data Generation

A perturbation-based synthetic dataset is constructed from the reference sp³s\* parameters of [Klimeck et al. (2000)](https://doi.org/10.1006/spmi.2000.0862):

```
θ_perturbed = θ_reference ⊙ (1 + ε),    ε ~ U(-0.04, +0.04)
```

For each perturbed parameter set, the 20×20 sp³s\* Hamiltonian (with spin-orbit coupling) is diagonalized at Γ, X, and L points to extract observable quantities.

### Input Features

| # | Feature Set | Description |
|---|-------------|-------------|
| **6-feat** | Baseline | Eg(Γ), Eg(X), Eg(L), Δso, me*, a₀ |
| **12-feat** | Physics-informed | Baseline + ΔEN, log(Z⁴), Phillips ionicity, direct/indirect flag, Eg(X)/Eg(Γ), Harrison V₀ |

### Evaluation

Models are evaluated under **stratified 5-fold cross-validation** against experimental band parameters from [Vurgaftman et al. (2001)](https://doi.org/10.1063/1.1368156).

---

## Key Results

**Eg(Γ) — Band Gap Prediction (eV):**

| Material | Exp. | SVR-12 | GBR-6 | MLP-12 |
|----------|------|--------|-------|--------|
| GaAs | 1.424 | 1.426 | 1.418 | 1.334 |
| InAs | 0.370 | 0.360 | 0.366 | 0.349 |
| GaSb | 0.750 | 0.750 | 0.753 | 0.742 |
| InSb | 0.169 | 0.161 | 0.163 | 0.172 |

> **Note on GaP:** As an indirect-gap material, GaP shows systematic deviations across all models. This reflects a known structural limitation of the sp³s\* basis — not a deficiency of the ML approach.

---

## References

1. **Klimeck, G.** et al. (2000). sp3s\* Tight-binding parameters for transport simulations in compound semiconductors. *Superlattices and Microstructures*, 27(5), 519–524. [DOI](https://doi.org/10.1006/spmi.2000.0862)
2. **Vurgaftman, I.** et al. (2001). Band parameters for III–V compound semiconductors and their alloys. *J. Appl. Phys.*, 89(11), 5815–5875. [DOI](https://doi.org/10.1063/1.1368156)
3. **Vogl, P.** et al. (1983). A semi-empirical tight-binding theory of the electronic structure of semiconductors. *J. Phys. Chem. Solids*, 44(5), 365–378. [DOI](https://doi.org/10.1016/0022-3697(83)90064-1)
4. **Harrison, W.A.** (1989). *Electronic Structure and the Properties of Solids.* Dover Publications.
5. **Soccodato, D.** et al. (2024). Machine learned environment-dependent corrections for a spds\* empirical tight-binding basis. *Mach. Learn.: Sci. Technol.*, 5, 025034. [DOI](https://doi.org/10.1088/2632-2153/ad4510)

---

## Citation

If you use this code in your research, please cite:

```bibtex
@inproceedings{malkoc2026ml_tb,
  author    = {Malko\c{c}, Derya and Ho\c{s}avc{\i}, Reyhan},
  title     = {Investigation of Machine Learning Models for sp$^3$s$^*$ 
               Tight-Binding Parameter Prediction in {III-V} Binary Semiconductors},
  booktitle = {International Semiconductor Conference – CAS 2026},
  year      = {2026},
  note      = {Submitted}
}
```

---

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

---
---

# 🇹🇷 Türkçe

## Genel Bakış

Bu depo, dokuz III-V ikili yarıiletken için sp³s\* sıkı-bağ (tight-binding) parametrelerini, yalnızca deneysel olarak ölçülebilir büyüklüklerden (bant aralığı, spin-yörünge ayrımı, etkin kütle, örgü sabiti) tahmin eden bir makine öğrenmesi çerçevesi sunar. DFT hesaplaması gerektirmez.

### Hızlı Başlangıç

```bash
git clone https://github.com/reyhanhosavci/ML-TightBinding-IIIV.git
cd ML-TightBinding-IIIV
pip install -r requirements.txt
python comparison_all.py
```

### Yöntem

- **Eğitim verisi:** Klimeck et al. (2000) referans parametrelerine ±%4 pertürbasyon uygulanarak 4.500 sentetik örnek üretilir.
- **Girdi özellikleri:** 6 özellikli temel set (Eg, Eg_X, Eg_L, Δso, me\*, a₀) ve 6 ek fizik-bilgili tanımlayıcıyla genişletilmiş 12 özellikli set.
- **Modeller:** SVR (RBF çekirdek), GBR (Gradient Boosting) ve MLP (Yapay Sinir Ağı).
- **Değerlendirme:** Vurgaftman et al. (2001) deneysel hedeflerine karşı 5-katlı katmanlı çapraz doğrulama.

### Temel Sonuçlar

| Hedef | En İyi Model | MAPE |
|-------|-------------|------|
| Eg(Γ) | SVR-12feat | %1.2 |
| Δso | GBR-12feat | %0.9 |
| me* | MLP-12feat | %4.2 |

> **GaP notu:** GaP, dolaylı bant aralıklı bir malzeme olduğundan, sp³s\* modeli çerçevesinde tüm modellerde sistematik sapma gösterir. Bu, ML yaklaşımının değil, TB modelinin yapısal bir kısıtlamasıdır.

### Dosya Yapısı

| Dosya | Açıklama |
|-------|----------|
| `comparison_all.py` | Ana karşılaştırma pipeline'ı |
| `physics_features.py` | 12 özellikli fizik-bilgili tanımlayıcı hesaplama |
| `harrison.py` | Harrison evrensel TB parametre hesaplayıcı |
| `data/results_table.csv` | Malzeme bazlı tahmin sonuçları |
| `data/tb_params_svr.csv` | TB parametreleri: Klimeck vs SVR tahmini |

### İletişim

- **Derya Malkoç** — dmalkoc@fsm.edu.tr
- **Reyhan Hoşavcı** — rgurleyen@fsm.edu.tr

Fatih Sultan Mehmet Vakıf Üniversitesi, İstanbul
