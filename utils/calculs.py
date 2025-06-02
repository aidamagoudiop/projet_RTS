

import pandas as pd

def calculs_principaux(csv_path):
    df = pd.read_csv(csv_path)
    ligne = df.iloc[0]

    population = ligne['population']
    surface = ligne['surface_km2']
    trafic_moyen = ligne['trafic_moyen_mbps']

    densite = population / surface
    debit_total = population * trafic_moyen  # en Mbps
    capacite_cellule = 100  # Mbps par cellule (hypothèse)
    nb_sites = int(debit_total / capacite_cellule) + 1

    return {
        "Zone": ligne['zone'],
        "Population": population,
        "Surface (km²)": surface,
        "Densité (hab/km²)": round(densite, 2),
        "Trafic moyen par utilisateur (Mbps)": trafic_moyen,
        "Débit total requis (Mbps)": round(debit_total, 2),
        "Capacité cellulaire (Mbps/site)": capacite_cellule,
        "Nombre de sites requis": nb_sites
    }
