import pandas as pd
from fpdf import FPDF
import zipfile
import os
import tempfile
import io

def export_excel(resultats, fichier="resultats.xlsx"):
    df = pd.DataFrame(list(resultats.items()), columns=["Paramètre", "Valeur"])
    df.to_excel(fichier, index=False)
    return fichier

def export_pdf(resultats, fichier="resultats.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Rapport de dimensionnement LTE", ln=True, align='C')
    pdf.ln(10)
    for k, v in resultats.items():
        pdf.cell(200, 10, txt=f"{k} : {v}", ln=True)
    pdf.output(fichier)
    return fichier

def creer_export_zip(files, output="export_projet.zip"):
    with tempfile.TemporaryDirectory() as tmpdirname:
        fichiers_a_zipper = []

        for i, f in enumerate(files):
            if isinstance(f, str):
                fichiers_a_zipper.append(f)
            elif isinstance(f, io.BytesIO):
                temp_path = os.path.join(tmpdirname, f"tempfile_{i}.png")
                with open(temp_path, "wb") as tmpfile:
                    tmpfile.write(f.getbuffer())
                fichiers_a_zipper.append(temp_path)
            else:
                raise ValueError(f"Type de fichier non supporté: {type(f)}")

        with zipfile.ZipFile(output, 'w') as zipf:
            for file_path in fichiers_a_zipper:
                zipf.write(file_path, os.path.basename(file_path))

    return output
