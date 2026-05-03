"""
initial_conditions.py — Conditions initiales
============================================
Fonctions pour générer la distribution de température initiale.
"""

import numpy as np

def gaussian_blob(grid, center_x: float, center_y: float, radius: float, max_temp: float = 100.0, bg_temp: float = 0.0) -> np.ndarray:
    """
    Crée un point chaud gaussien (une "tache" de chaleur) au centre spécifié.
    """
    T = np.full(grid.shape, bg_temp)
    dist_sq = (grid.X - center_x)**2 + (grid.Y - center_y)**2
    T += max_temp * np.exp(-dist_sq / (radius**2))
    return T

def uniform_temperature(grid, temp: float = 0.0) -> np.ndarray:
    """
    Crée une distribution de température uniforme.
    """
    return np.full(grid.shape, temp)
