import matplotlib.pyplot as plt
import io
import numpy as np
from PIL import Image

def graphe_sites(nombre_cellules, sites_existants=0):
    sites_a_construire = max(0, nombre_cellules - sites_existants)

    categories = ['Existants', 'À construire']
    valeurs = [sites_existants, sites_a_construire]
    couleurs = ['#1f77b4', '#ff7f0e']

    fig, ax = plt.subplots(figsize=(5,4))
    bars = ax.bar(categories, valeurs, color=couleurs)
    ax.set_ylabel("Nombre de sites")
    ax.set_title("Distribution des sites cellulaires")

    for bar in bars:
        hauteur = bar.get_height()
        ax.annotate(f'{int(hauteur)}',
                    xy=(bar.get_x() + bar.get_width() / 2, hauteur),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=10)

    ax.legend(bars, categories)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    image = Image.open(buf)
    return image


def graphe_trafic(trafic_moyen):
    heures = np.arange(24)
    trafic = trafic_moyen * (0.5 + 0.5 * np.sin((heures / 24) * 2 * np.pi))

    seuil = trafic_moyen * 0.8

    fig, ax = plt.subplots(figsize=(6,4))
    ax.plot(heures, trafic, marker='o', color='#2ca02c', label="Trafic horaire")
    ax.axhline(seuil, color='r', linestyle='--', label="Seuil critique")

    ax.fill_between(heures, trafic, seuil, where=(trafic > seuil), color='red', alpha=0.3)
    ax.set_xlabel("Heure")
    ax.set_ylabel("Trafic (Erlang)")
    ax.set_title("Évolution du trafic sur 24h")
    ax.legend()
    ax.grid(True)

    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    image = Image.open(buf)
    return image
