"""
explicit_euler.py — Schéma d'Euler Explicite (FTCS)
===================================================
Résolution par la méthode des différences finies explicite.
"""

import numpy as np
from .base_solver import BaseSolver

class ExplicitEulerSolver(BaseSolver):
    def __init__(self, grid, alpha: float, dt: float, bc):
        super().__init__(grid, alpha, dt)
        self.bc = bc
        
        # Nombres de Courant en x et y
        self.rx = (self.alpha * self.dt) / (self.grid.dx**2)
        self.ry = (self.alpha * self.dt) / (self.grid.dy**2)
        
        # Vérification du critère de stabilité (CFL)
        if self.rx + self.ry > 0.5:
            raise ValueError(
                f"Instabilité détectée ! Le schéma d'Euler Explicite n'est pas stable.\n"
                f"rx + ry = {self.rx + self.ry:.4f} > 0.5\n"
                f"Solution : Réduisez le pas de temps 'dt' ou augmentez 'dx'/'dy'."
            )
            
    def step(self):
        """Effectue un pas de temps avec le schéma FTCS."""
        T_new = self.T.copy()
        
        # Discrétisation spatiale centrée et temporelle avant (FTCS)
        # On utilise le slicing numpy pour éviter les boucles (beaucoup plus rapide)
        T_new[1:-1, 1:-1] = self.T[1:-1, 1:-1] + \
                            self.rx * (self.T[2:, 1:-1] - 2*self.T[1:-1, 1:-1] + self.T[:-2, 1:-1]) + \
                            self.ry * (self.T[1:-1, 2:] - 2*self.T[1:-1, 1:-1] + self.T[1:-1, :-2])
                            
        # Appliquer les conditions aux limites
        self.T = self.bc.apply(T_new)
