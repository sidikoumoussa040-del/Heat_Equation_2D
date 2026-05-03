"""
boundary.py — Conditions aux limites
====================================
Définit les conditions aux limites pour la simulation (Dirichlet, Neumann...).
"""

import numpy as np

class BoundaryCondition:
    """Classe de base pour les conditions aux limites."""
    def apply(self, T: np.ndarray) -> np.ndarray:
        raise NotImplementedError


class DirichletBC(BoundaryCondition):
    """
    Condition aux limites de Dirichlet (Température imposée et constante sur les bords).
    """
    def __init__(self, value: float = 0.0):
        self.value = value

    def apply(self, T: np.ndarray) -> np.ndarray:
        T_new = T.copy()
        T_new[0, :] = self.value   # Bord gauche (x=0)
        T_new[-1, :] = self.value  # Bord droit (x=Lx)
        T_new[:, 0] = self.value   # Bord bas (y=0)
        T_new[:, -1] = self.value  # Bord haut (y=Ly)
        return T_new
