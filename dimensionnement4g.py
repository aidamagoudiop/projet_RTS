import math
import folium
import pandas as pd
import gradio as gr
from fpdf import FPDF
import tempfile
import os

# ===== Calcul de rayon par environnement =====
def get_rayon_par_environment(environnement):
    return {"Rural": 3.0, "Suburbain": 1.5, "Urbain": 0.8}.get(environnement, 2.0)

# ===== Calcul du dimensionnement LTE =====
def calculer_dimensionnement(population, penetration, trafic, debit, capacite, environnement):
    population_active = population * (penetration / 100)
    trafic_total = round(population_active * trafic, 2)
    debit_total = round(population_active * debit, 2)
    
    rayon = get_rayon_par_environment(environnement)
    surface_cellule = round((3 * math.sqrt(3) / 2) * rayon**2, 2)
    surface_totale_km2 = 100
    nombre_cellules_calc = math.ceil(surface_totale_km2 / surface_cellule)
    capacite_totale = round(nombre_cellules_calc * capacite, 2)
    
    saturation = " Capacité suffisante" if debit_total <= capacite_totale else " Saturation - Densification recommandée"
    recommandation = "Réseau optimal" if debit_total <= capacite_totale else "Augmenter le nombre de cellules ou la capacité par cellule"
    
    nombre_sites = math.ceil(nombre_cellules_calc / 3)

    return {
        "Environnement": environnement,
        "Population totale": population,
        "Taux de pénétration (%)": penetration,
        "Population active": int(population_active),
        "Trafic total (Erlang)": trafic_total,
        "Débit total (Mbps)": debit_total,
        "Surface cellule (km²)": surface_cellule,
        "Nombre de cellules nécessaires": nombre_cellules_calc,
        "Capacité totale (Mbps)": capacite_totale,
        "Saturation": saturation,
        "Recommandation": recommandation,
        "Nombre de sites (eNodeB)": nombre_sites
    }

# ===== Génération des fichiers exports =====
def export_excel(resultats):
    path = tempfile.mktemp(suffix=".xlsx")
    pd.DataFrame(resultats.items(), columns=["Paramètre", "Valeur"]).to_excel(path, index=False)
    return path

def export_pdf(resultats):
    path = tempfile.mktemp(suffix=".pdf")
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt="Rapport de Dimensionnement 4G LTE", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    for k, v in resultats.items():
        pdf.cell(0, 10, f"{k}: {v}", ln=True)
    pdf.output(path)
    return path

# ===== Interface Gradio principale =====
def lancer_dimensionnement(population, penetration, trafic, debit, capacite, environnement):
    resultats = calculer_dimensionnement(population, penetration, trafic, debit, capacite, environnement)
    
    excel_path = export_excel(resultats)
    pdf_path = export_pdf(resultats)
    
    texte_resultats = "\n".join([f"{k}: {v}" for k, v in resultats.items()])
    return texte_resultats, excel_path, pdf_path

with gr.Blocks(title=" Dimensionnement 4G LTE PRO (local)") as demo:
    gr.Markdown("# 📶 Dimensionnement 4G LTE")
    gr.Markdown("💡 Saisissez les paramètres et obtenez le dimensionnement automatique.")

    with gr.Row():
        population = gr.Number(label="Population", value=50000)
        penetration = gr.Number(label="Taux de pénétration (%)", value=70)
        environnement = gr.Dropdown(label="Type d'environnement", choices=["Rural", "Suburbain", "Urbain"], value="Rural")
    
    with gr.Row():
        trafic = gr.Number(label="Trafic moyen (Erlang)", value=0.025)
        debit = gr.Number(label="Débit moyen (Mbps)", value=0.15)
        capacite = gr.Number(label="Capacité cellulaire (Mbps)", value=15.0)

    bouton = gr.Button(" Calculer")

    resultat_text = gr.Textbox(label="📊 Résultats détaillés", lines=15)
    fichier_excel = gr.File(label="📥 Excel")
    fichier_pdf = gr.File(label="📥 PDF")

    bouton.click(
        fn=lancer_dimensionnement,
        inputs=[population, penetration, trafic, debit, capacite, environnement],
        outputs=[resultat_text, fichier_excel, fichier_pdf]
    )

demo.launch(share=True)

