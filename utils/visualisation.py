import matplotlib.pyplot as plt
import os

def generer_carte_couverture(data):
    nb_sites = data["Nombre de sites requis"]
    surface = data["Surface (km²)"]

    densite_site = nb_sites / surface

    fig, ax = plt.subplots()
    ax.bar(["Densité de sites (sites/km²)"], [densite_site], color="skyblue")
    ax.set_ylabel("Sites/km²")
    ax.set_title("Carte de couverture approximative")

    output_path = "output/carte_couverture.png"
    os.makedirs("output", exist_ok=True)
    plt.savefig(output_path)
    plt.close()
