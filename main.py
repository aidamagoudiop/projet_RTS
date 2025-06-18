import gradio as gr
from models import ProjetManager
from calculs import calculer_dimensionnement
from exports import export_excel, export_pdf, creer_export_zip
from maps import generer_carte_multicouches
from visuals import graphe_sites, graphe_trafic
from suggestions import generer_suggestions

import tempfile
import os

projet_manager = ProjetManager("database.json")

def creer_projet(pseudo, nom, description, pays, ville):
    success, msg = projet_manager.creer_projet(pseudo, nom, description, pays, ville)
    projets = projet_manager.lister_projets(pseudo)
    return projets, msg

def calculer(pseudo, projet, population, penetration, trafic, debit, capacite, environnement):
    resultats = calculer_dimensionnement(population, penetration, trafic, debit, capacite, environnement)
    projet_manager.maj_resultats(pseudo, projet, resultats)
    excel_path = export_excel(resultats)
    pdf_path = export_pdf(resultats)
    return resultats, excel_path, pdf_path

with gr.Blocks(theme=gr.themes.Monochrome(), title="LTE Planner PRO V2.6") as app:
    gr.Markdown("## 📶 LTE Planner PRO V2.6 — Multi-layer Coverage ✅")

    with gr.Row():
        pseudo = gr.Textbox(label="👤 Votre nom", scale=1)
        projet = gr.Dropdown(label="📁 Sélectionnez un projet", scale=2)
        btn_charger = gr.Button("🔄 Charger projets")

    with gr.Accordion("➕ Créer un nouveau projet", open=False):
        nom = gr.Textbox(label="Nom du projet")
        description = gr.Textbox(label="Description")
        pays = gr.Textbox(label="Pays")
        ville = gr.Textbox(label="Ville")
        btn_creer = gr.Button("Créer projet")
        msg = gr.Textbox(interactive=False)

    def charger(pseudo_value):
        projets = projet_manager.lister_projets(pseudo_value)
        return gr.update(choices=projets), ""

    btn_charger.click(charger, inputs=pseudo, outputs=[projet, msg])
    btn_creer.click(creer_projet, inputs=[pseudo, nom, description, pays, ville], outputs=[projet, msg])

    gr.Markdown("### 📊 Paramètres de simulation")

    with gr.Row():
        population = gr.Number(label="Population", value=50000)
        penetration = gr.Number(label="Pénétration (%)", value=70)
        trafic = gr.Number(label="Trafic (Erlang)", value=0.025)
        debit = gr.Number(label="Débit (Mbps)", value=0.15)
        capacite = gr.Number(label="Capacité cellulaire (Mbps)", value=15)

    environnement = gr.Dropdown(choices=["Rural", "Suburbain", "Urbain"], label="Environnement", value="Rural")
    latitude = gr.Number(label="Latitude (°)", value=14.7167)
    longitude = gr.Number(label="Longitude (°)", value=-17.4677)
    rayon_micro = gr.Number(label="Rayon Small-cell (km)", value=0.5)

    btn_calcul = gr.Button("🚀 Calculer dimensionnement")

    resultats = gr.Textbox(label="📄 Résultats détaillés", lines=10)
    excel_file = gr.File(label="📥 Excel")
    pdf_file = gr.File(label="📥 PDF")
    map_html = gr.HTML(label="🗺 Visualisation carte multicouche")
    sites_graph = gr.Image(label="Graphique sites")
    trafic_graph = gr.Image(label="Graphique trafic")
    zip_file = gr.File(label="📦 Export complet ZIP")
    suggestions_box = gr.Textbox(label="💡 Suggestions pour l'ingénieur", lines=8, interactive=False)

    def afficher_resultat(pseudo, projet, population, penetration, trafic, debit, capacite, environnement, latitude, longitude, rayon_micro):
        res, excel, pdf = calculer(pseudo, projet, population, penetration, trafic, debit, capacite, environnement)
        texte = "\n".join([f"{k}: {v}" for k, v in res.items()])
        rayon_macro = res['Rayon Cellule (km)']

        carte_html = generer_carte_multicouches(latitude, longitude, rayon_macro, rayon_micro)
        graph_sites = graphe_sites(res['Nombre Cellules'])
        graph_trafic = graphe_trafic(trafic)

        # On sauvegarde les images temporairement pour le zip
        temp_dir = tempfile.mkdtemp()
        graph_sites_path = os.path.join(temp_dir, "sites.png")
        graph_sites.save(graph_sites_path)
        graph_trafic_path = os.path.join(temp_dir, "trafic.png")
        graph_trafic.save(graph_trafic_path)

        zip_path = creer_export_zip([excel, pdf, graph_sites_path, graph_trafic_path])
        suggestions = generer_suggestions(res)

        return texte, excel, pdf, carte_html, graph_sites, graph_trafic, zip_path, suggestions

    btn_calcul.click(
        afficher_resultat,
        inputs=[pseudo, projet, population, penetration, trafic, debit, capacite, environnement, latitude, longitude, rayon_micro],
        outputs=[resultats, excel_file, pdf_file, map_html, sites_graph, trafic_graph, zip_file, suggestions_box]
    )

app.launch()
