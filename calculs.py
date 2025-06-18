import math

def calculer_dimensionnement(population, penetration, trafic, debit, capacite, environnement):
    pop_active = population * (penetration / 100)
    trafic_total = pop_active * trafic
    debit_total = pop_active * debit

    facteur_environnement = {"Rural": 5, "Suburbain": 3, "Urbain": 1}[environnement]
    superficie = population / facteur_environnement

    nb_sites_trafic = math.ceil(debit_total / capacite)
    rayon_cellule = math.sqrt(superficie / (math.pi * nb_sites_trafic))
    nb_sites_surface = math.ceil(superficie / (math.pi * rayon_cellule**2))

    nb_total_sites = max(nb_sites_trafic, nb_sites_surface)

    return {
        "Population active": int(pop_active),
        "Trafic total (Erlang)": round(trafic_total, 2),
        "Débit total (Mbps)": round(debit_total, 2),
        "Superficie estimée (km²)": round(superficie, 2),
        "Rayon Cellule (km)": round(rayon_cellule, 2),
        "Nombre Cellules": nb_total_sites
    }
