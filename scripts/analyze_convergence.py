"""
analyze_convergence.py
======================
Script pour générer la figure de convergence (Erreur vs dt) pour la méthode d'Euler Explicite.
L'image produite pourra être intégrée dans le rapport LaTeX.
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.grid import Grid2D
from src.core.boundary import DirichletBC
from src.core.initial_conditions import fundamental_mode
from src.methods.explicit_euler import ExplicitEulerSolver

def compute_error(grid, dt, num_steps, alpha=0.01):
    T0 = fundamental_mode(grid, max_temp=100.0)
    bc = DirichletBC(value=0.0)
    T0 = bc.apply(T0)
    
    solver = ExplicitEulerSolver(grid=grid, alpha=alpha, dt=dt, bc=bc)
    solver.set_initial_condition(T0)
    solver.run(num_steps)
    
    t_final = num_steps * dt
    T_exact = 100.0 * np.sin(np.pi * grid.X / grid.Lx) * np.sin(np.pi * grid.Y / grid.Ly) * \
              np.exp(-alpha * np.pi**2 * (1.0/grid.Lx**2 + 1.0/grid.Ly**2) * t_final)
              
    error = np.max(np.abs(solver.T - T_exact))
    return error

def main():
    print("Calcul de l'erreur pour différents pas de temps (dt)...")
    
    # On garde le maillage spatial constant pour isoler l'erreur temporelle
    grid = Grid2D(Lx=1.0, Ly=1.0, Nx=20, Ny=20)
    
    # Différentes valeurs de dt (doivent respecter la CFL)
    dt_values = [0.005, 0.002, 0.001, 0.0005, 0.0002]
    t_final_target = 0.5 
    
    errors = []
    
    for dt in dt_values:
        num_steps = int(t_final_target / dt)
        err = compute_error(grid, dt, num_steps)
        errors.append(err)
        print(f" -> dt = {dt:.4f}s \t Erreur Max = {err:.4e}")
        
    # Tracé de la courbe de convergence
    plt.figure(figsize=(8, 6))
    plt.loglog(dt_values, errors, 'o-', linewidth=2, markersize=8, color='crimson', label='Erreur Numérique ($L_\infty$)')
    
    # Ligne de référence d'Ordre 1 : O(dt)
    # On la cale sur le dernier point pour bien comparer la pente
    ref_line = np.array(dt_values) * (errors[-1] / dt_values[-1])
    plt.loglog(dt_values, ref_line, 'k--', label='Ordre théorique: O($\Delta t$)')
    
    plt.xlabel('Pas de temps $\Delta t$ (s)')
    plt.ylabel('Erreur Maximale par rapport à la solution exacte')
    plt.title('Convergence en temps - Schéma d'Euler Explicite')
    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.legend()
    
    os.makedirs("results/figures", exist_ok=True)
    save_path = "results/figures/convergence_explicite.png"
    plt.savefig(save_path, bbox_inches='tight', dpi=300)
    print(f"\nFigure de convergence générée et sauvegardée dans : {save_path}")
    print("Cette figure est prête à être intégrée dans le fichier LaTeX !")

if __name__ == "__main__":
    main()
