"""
plot_2d.py — Outils de visualisation
====================================
Fonctions pour générer des cartes de chaleur statiques et animées.
"""

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np

def plot_heatmap(grid, T, title="Température", save_path=None):
    """Affiche une carte de chaleur statique."""
    plt.figure(figsize=(8, 6))
    plt.contourf(grid.X, grid.Y, T, levels=50, cmap='inferno')
    plt.colorbar(label='Température')
    plt.title(title)
    plt.xlabel('x')
    plt.ylabel('y')
    
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
        print(f"Image sauvegardée: {save_path}")
        
    plt.close() # Ne pas afficher si on ne fait que sauvegarder


def animate_heatmap(grid, history, dt, step_interval=1, save_path=None):
    """
    Génère une animation de l'évolution de la température.
    
    Paramètres:
    - step_interval: Prend 1 image tous les `step_interval` pas de temps
                     pour accélérer la création de la vidéo.
    """
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Trouver le min et le max globaux pour fixer l'échelle de couleur
    T_min = min([np.min(T) for T in history])
    T_max = max([np.max(T) for T in history])
    
    # Affichage initial
    cax = ax.contourf(grid.X, grid.Y, history[0], levels=50, cmap='inferno', vmin=T_min, vmax=T_max)
    fig.colorbar(cax, label='Température')
    
    # Images à utiliser pour l'animation
    frames_to_plot = list(range(0, len(history), step_interval))
    if frames_to_plot[-1] != len(history) - 1:
        frames_to_plot.append(len(history) - 1)
        
    def update(frame_idx):
        ax.clear()
        T = history[frame_idx]
        cax = ax.contourf(grid.X, grid.Y, T, levels=50, cmap='inferno', vmin=T_min, vmax=T_max)
        
        temps_reel = frame_idx * dt
        ax.set_title(f"Temps = {temps_reel:.4f} s")
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        return cax,
        
    anim = FuncAnimation(fig, update, frames=frames_to_plot, interval=50, blit=False)
    
    if save_path:
        if save_path.endswith('.gif'):
            writer = PillowWriter(fps=15)
        else:
            writer = 'ffmpeg' # Nécessite d'avoir ffmpeg installé
        
        print(f"Génération de l'animation en cours ({len(frames_to_plot)} images)...")
        anim.save(save_path, writer=writer)
        print(f"Animation sauvegardée: {save_path}")
        
    plt.close()
