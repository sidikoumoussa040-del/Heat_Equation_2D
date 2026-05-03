"""
run_simulation.py — Lancement de la méthode d'Euler Explicite
=============================================================
Script principal pour exécuter la simulation de la diffusion de chaleur.
"""

import os
import sys

# Ajouter le répertoire racine du projet au PATH Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.grid import Grid2D
from src.core.boundary import DirichletBC
from src.core.initial_conditions import gaussian_blob
from src.methods.explicit_euler import ExplicitEulerSolver
from src.visualization.plot_2d import plot_heatmap, animate_heatmap

def main():
    # 1. Configuration du domaine (Plaque de 1m x 1m, 50x50 points de calcul)
    print("1. Création de la grille...")
    grid = Grid2D(Lx=1.0, Ly=1.0, Nx=50, Ny=50)
    
    # 2. Condition Initiale: Tache très chaude (100°C) au milieu d'une plaque froide (10°C)
    print("2. Mise en place des conditions initiales...")
    T0 = gaussian_blob(grid, center_x=0.5, center_y=0.5, radius=0.1, max_temp=100.0, bg_temp=10.0)
    
    # 3. Condition aux Limites: Les bords sont maintenus froids (10°C)
    print("3. Configuration des conditions aux limites...")
    bc = DirichletBC(value=10.0)
    T0 = bc.apply(T0)
    
    # 4. Paramètres physiques et numériques
    alpha = 0.01  # Diffusivité thermique
    dt = 0.001    # Pas de temps (DOIT respecter CFL)
    num_steps = 400 # Nombre total d'itérations
    
    print(f"4. Initialisation du solveur Euler Explicite (dt={dt}s)...")
    try:
        solver = ExplicitEulerSolver(grid=grid, alpha=alpha, dt=dt, bc=bc)
    except ValueError as e:
        print(f"\n[ERREUR] {e}")
        sys.exit(1)
        
    solver.set_initial_condition(T0)
    
    # 5. Exécution de la simulation
    print(f"5. Lancement du calcul pour {num_steps} pas de temps...")
    solver.run(num_steps)
    print("   -> Calcul terminé avec succès !")
    
    # 6. Sauvegarde des résultats
    print("6. Génération des visualisations...")
    os.makedirs("results/figures", exist_ok=True)
    os.makedirs("results/animations", exist_ok=True)
    
    # Sauvegarde de l'état final en image statique
    plot_heatmap(grid, solver.T, 
                 title=f"État final (t = {num_steps * dt:.3f} s)", 
                 save_path="results/figures/etat_final.png")
                 
    # Sauvegarde de l'animation GIF (on prend 1 image sur 5 pour accélérer)
    animate_heatmap(grid, solver.history, dt=dt, step_interval=5, 
                    save_path="results/animations/diffusion_chaleur.gif")
                    
    print("\n✅ Simulation complète ! Allez voir dans le dossier 'results/'.")

if __name__ == "__main__":
    main()
