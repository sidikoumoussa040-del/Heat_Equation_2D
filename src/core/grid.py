"""
grid.py — Grille de discrétisation 2D
=======================================
Définit la structure de la grille spatiale pour la simulation.
"""

import numpy as np


class Grid2D:
    """
    Grille uniforme 2D pour la discrétisation par différences finies.

    Paramètres
    ----------
    Lx : float
        Longueur du domaine en x (mètres)
    Ly : float
        Longueur du domaine en y (mètres)
    Nx : int
        Nombre de points intérieurs en x
    Ny : int
        Nombre de points intérieurs en y

    Attributs calculés
    ------------------
    dx, dy : float
        Pas d'espace en x et y
    x, y   : ndarray
        Coordonnées des nœuds (incluant les bords)
    X, Y   : ndarray (2D)
        Grilles meshgrid pour la visualisation
    """

    def __init__(self, Lx: float, Ly: float, Nx: int, Ny: int):
        if Lx <= 0 or Ly <= 0:
            raise ValueError("Les dimensions du domaine doivent être positives.")
        if Nx < 2 or Ny < 2:
            raise ValueError("Le nombre de points doit être >= 2.")

        self.Lx = Lx
        self.Ly = Ly
        self.Nx = Nx  # points intérieurs en x
        self.Ny = Ny  # points intérieurs en y

        # Pas d'espace (N+1 intervalles pour N+2 points avec bords)
        self.dx = Lx / (Nx + 1)
        self.dy = Ly / (Ny + 1)

        # Coordonnées incluant les bords
        self.x = np.linspace(0.0, Lx, Nx + 2)
        self.y = np.linspace(0.0, Ly, Ny + 2)

        # Meshgrid pour visualisation
        self.X, self.Y = np.meshgrid(self.x, self.y, indexing='ij')

    @property
    def shape(self):
        """Taille de la grille complète (avec bords) : (Nx+2, Ny+2)"""
        return (self.Nx + 2, self.Ny + 2)

    @property
    def interior_shape(self):
        """Taille de la grille intérieure : (Nx, Ny)"""
        return (self.Nx, self.Ny)

    def __repr__(self):
        return (
            f"Grid2D(Lx={self.Lx}, Ly={self.Ly}, "
            f"Nx={self.Nx}, Ny={self.Ny}, "
            f"dx={self.dx:.4f}, dy={self.dy:.4f})"
        )
