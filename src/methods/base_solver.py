"""
base_solver.py — Solveur de base
=================================
Classe parente abstraite pour toutes les méthodes de résolution.
"""

import numpy as np

class BaseSolver:
    def __init__(self, grid, alpha: float, dt: float):
        self.grid = grid
        self.alpha = alpha
        self.dt = dt
        
        self.T = None
        self.time = 0.0
        self.history = []
        
    def set_initial_condition(self, T0: np.ndarray):
        """Initialise la température et sauvegarde l'état initial."""
        self.T = T0.copy()
        self.time = 0.0
        self.history = [self.T.copy()]
        
    def step(self):
        """Avance d'un pas de temps. À implémenter dans les classes filles."""
        raise NotImplementedError("La méthode step() doit être redéfinie.")
        
    def run(self, num_steps: int):
        """Exécute la simulation sur un nombre donné de pas de temps."""
        if self.T is None:
            raise ValueError("Veuillez d'abord définir la condition initiale (set_initial_condition).")
            
        for _ in range(num_steps):
            self.step()
            self.time += self.dt
            self.history.append(self.T.copy())
