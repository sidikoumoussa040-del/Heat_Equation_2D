# 🔥 Simulation Numérique de l'Équation de la Chaleur 2D

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![NumPy](https://img.shields.io/badge/NumPy-1.24+-orange.svg)](https://numpy.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-3.7+-green.svg)](https://matplotlib.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-En%20cours-blueviolet)]()

## 📌 Description

Ce projet implémente et compare différentes méthodes numériques pour résoudre l'**équation de la chaleur en 2D** :

$$\frac{\partial u}{\partial t} = \alpha \left( \frac{\partial^2 u}{\partial x^2} + \frac{\partial^2 u}{\partial y^2} \right)$$

où $\alpha$ est la diffusivité thermique du matériau, sur un domaine $\Omega = [0, L_x] \times [0, L_y]$ avec des conditions initiales et aux limites données.

## 🎯 Objectifs

- Implémenter plusieurs schémas numériques (explicite, implicite, Crank-Nicolson, ADI...)
- Analyser la **stabilité**, la **précision** et le **coût computationnel** de chaque méthode
- Comparer les résultats avec des **solutions analytiques** (quand disponibles)
- Produire des visualisations claires et des rapports d'analyse

## 🗂️ Structure du Projet

```
Heat_Equation_2D/
│
├── README.md                   # Ce fichier
├── LICENSE                     # Licence MIT
├── requirements.txt            # Dépendances Python
├── .gitignore                  # Fichiers ignorés par Git
├── setup.py                    # Installation du package
│
├── docs/                       # Documentation
│   ├── theory/                 # Bases théoriques (PDF, LaTeX)
│   │   ├── equation_chaleur.md
│   │   └── stabilite_consistance.md
│   └── reports/                # Rapports d'analyse générés
│
├── src/                        # Code source principal
│   ├── __init__.py
│   ├── core/                   # Modules fondamentaux
│   │   ├── __init__.py
│   │   ├── grid.py             # Grille de discrétisation
│   │   ├── boundary.py         # Conditions aux limites
│   │   └── initial_conditions.py
│   │
│   ├── methods/                # Méthodes numériques
│   │   ├── __init__.py
│   │   ├── base_solver.py      # Classe abstraite de base
│   │   ├── explicit_euler.py   # ✅ Euler Explicite (Phase 1)
│   │   ├── implicit_euler.py   # 🔜 Euler Implicite (Phase 2)
│   │   ├── crank_nicolson.py   # 🔜 Crank-Nicolson (Phase 3)
│   │   └── adi.py              # 🔜 ADI - Alternating Direction Implicit (Phase 4)
│   │
│   ├── analysis/               # Outils d'analyse
│   │   ├── __init__.py
│   │   ├── stability.py        # Analyse de stabilité (CFL, Von Neumann)
│   │   ├── convergence.py      # Tests de convergence
│   │   ├── error_metrics.py    # Calcul des erreurs (L1, L2, Linf)
│   │   └── benchmark.py        # Comparaison des méthodes
│   │
│   └── visualization/          # Visualisation
│       ├── __init__.py
│       ├── plot_2d.py           # Cartes de chaleur 2D
│       ├── plot_convergence.py  # Courbes de convergence
│       └── animation.py         # Animations temporelles
│
├── notebooks/                  # Jupyter Notebooks d'exploration
│   ├── 01_euler_explicite.ipynb
│   ├── 02_euler_implicite.ipynb
│   ├── 03_crank_nicolson.ipynb
│   └── 04_comparaison_methodes.ipynb
│
├── tests/                      # Tests unitaires
│   ├── __init__.py
│   ├── test_grid.py
│   ├── test_boundary.py
│   ├── test_explicit_euler.py
│   └── test_error_metrics.py
│
├── configs/                    # Fichiers de configuration
│   ├── default.yaml
│   └── benchmark.yaml
│
├── results/                    # Résultats de simulation (ignorés par Git)
│   ├── figures/
│   ├── animations/
│   └── data/
│
└── scripts/                    # Scripts d'exécution principaux
    ├── run_simulation.py
    ├── run_benchmark.py
    └── generate_report.py
```

## 🧪 Scénario Modélisé (Phase 1)

Pour notre première phase d'expérimentation, la simulation reproduit le scénario physique suivant :

- **Domaine Spatial ($\Omega$)** : Plaque carrée de dimension $L_x = 1.0$ m et $L_y = 1.0$ m.
- **Conditions aux Limites (Dirichlet)** : Les bords de la plaque sont maintenus à une température froide constante.
  $$T(0,y,t) = T(L_x,y,t) = T(x,0,t) = T(x,L_y,t) = 10\text{°C}$$
- **Condition Initiale** : Une tache de chaleur intense (profil gaussien) déposée au centre de la plaque froide.
  $$T(x,y,0) = 10 + 100 \cdot \exp\left(-\frac{(x - 0.5)^2 + (y - 0.5)^2}{0.1^2}\right)$$
- **Solution Exacte Analytique** : La solution exacte de ce problème (avec $u = T - 10$ pour avoir des bords homogènes) se décompose en série de Fourier double (fonctions propres du laplacien sur un carré) :
  $$T(x,y,t) = 10 + \sum_{m=1}^{\infty} \sum_{n=1}^{\infty} A_{mn} \sin(m \pi x) \sin(n \pi y) \cdot e^{-\alpha \pi^2 (m^2 + n^2) t}$$
  où les coefficients $A_{mn}$ s'obtiennent par projection de la condition initiale sur la base des sinus :
  $$A_{mn} = 4 \int_{0}^{1} \int_{0}^{1} \left( T(x,y,0) - 10 \right) \sin(m \pi x) \sin(n \pi y) \, dx \, dy$$

## 🚀 Méthodes Numériques Implémentées

| Phase | Méthode | Schéma | Stabilité | Ordre (espace) | Ordre (temps) | Statut |
|-------|---------|--------|-----------|----------------|---------------|--------|
| 1 | **Euler Explicite** | FTCS | Conditionnelle ($r \leq \frac{1}{4}$) | O(Δx²) | O(Δt) | ✅ Implémenté |
| 2 | **Euler Implicite** | BTCS | Inconditionnelle | O(Δx²) | O(Δt) | 🔜 Planifié |
| 3 | **Crank-Nicolson** | CN | Inconditionnelle | O(Δx²) | O(Δt²) | 🔜 Planifié |
| 4 | **ADI** | Peaceman-Rachford | Inconditionnelle | O(Δx²) | O(Δt²) | 🔜 Planifié |

## ⚙️ Installation

```bash
# Cloner le dépôt
git clone https://github.com/<votre-username>/Heat_Equation_2D.git
cd Heat_Equation_2D

# Créer un environnement virtuel
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac

# Installer les dépendances
pip install -r requirements.txt
```

## 🔧 Utilisation Rapide

```python
from src.core.grid import Grid2D
from src.core.boundary import DirichletBC
from src.methods.explicit_euler import ExplicitEulerSolver

# Définir la grille
grid = Grid2D(Lx=1.0, Ly=1.0, Nx=50, Ny=50)

# Conditions aux limites (Dirichlet homogènes)
bc = DirichletBC(grid, value=0.0)

# Solveur
solver = ExplicitEulerSolver(grid=grid, bc=bc, alpha=0.01, dt=0.001)

# Lancer la simulation
solver.run(T_final=0.5)
solver.plot()
```

Ou via script :
```bash
python scripts/run_simulation.py --method explicit_euler --config configs/default.yaml
```

## 📊 Analyses Disponibles

- **Stabilité** : Critère CFL, analyse de Von Neumann
- **Convergence** : Convergence en espace et en temps (ordre empirique)
- **Erreurs** : Normes L1, L2, L∞ par rapport à la solution analytique
- **Performance** : Temps CPU, mémoire, scalabilité

## 📖 Références Théoriques

- Strikwerda, J.C. (2004). *Finite Difference Schemes and Partial Differential Equations*
- LeVeque, R.J. (2007). *Finite Difference Methods for Ordinary and Partial Differential Equations*
- Morton, K.W. & Mayers, D.F. (2005). *Numerical Solution of Partial Differential Equations*

## 👤 Auteur

**Sidik** — Projet de Simulation Numérique  
📅 2026

## 📄 Licence

Ce projet est sous licence MIT — voir le fichier [LICENSE](LICENSE) pour plus de détails.
