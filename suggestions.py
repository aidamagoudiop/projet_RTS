def generer_suggestions(resultats):
    suggestions = []

    nb_sites = resultats.get("Nombre Cellules", 0)
    superficie = resultats.get("Superficie estimée (km²)", 0)
    rayon = resultats.get("Rayon Cellule (km)", 0)
    trafic = resultats.get("Trafic total (Erlang)", 0)
    debit = resultats.get("Débit total (Mbps)", 0)

    if nb_sites > 200:
        suggestions.append("⚠️ Le nombre de sites est très élevé, envisagez une optimisation du plan de fréquence ou du schéma de réutilisation.")
    elif nb_sites < 5:
        suggestions.append("✅ La densité de sites semble raisonnable pour ce scénario.")

    if rayon > 5:
        suggestions.append("ℹ️ Le rayon des cellules est grand. Vérifiez la disponibilité des ressources de fréquence basse (ex: LTE 700 MHz).")
    elif rayon < 1:
        suggestions.append("⚠️ Les cellules sont très petites, il faudra prévoir un déploiement dense avec des small cells.")

    if debit > 500:
        suggestions.append("⚠️ Le trafic total est très élevé. Vérifiez les capacités du réseau cœur et de backhaul.")
    
    if superficie > 1000:
        suggestions.append("ℹ️ Superficie très large, envisagez une solution mixte (Macro / Micro / Sat).")

    if not suggestions:
        suggestions.append("✅ Aucun problème majeur détecté sur ce dimensionnement.")

    return "\n".join(suggestions)
