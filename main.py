from utils.calculs import calculs_principaux
from utils.visualisation import generer_carte_couverture
from utils.rapport import generer_rapport_pdf

def main():
    print("📡 Dimensionnement Réseau 4G LTE pour Kaffrine")
    
    # Chargement et calculs
    resultats = calculs_principaux("data/zone.csv")

    # Affichage des résultats
    for cle, val in resultats.items():
        print(f"{cle} : {val}")

    # Génération des visualisations et du rapport
    generer_carte_couverture(resultats)
    generer_rapport_pdf(resultats)
    print("✅ Rapport généré dans output/rapport.pdf")

if __name__ == "__main__":
    main()
