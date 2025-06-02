from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os

def generer_rapport_pdf(data):
    os.makedirs("output", exist_ok=True)
    c = canvas.Canvas("output/rapport.pdf", pagesize=A4)
    c.setFont("Helvetica", 12)

    c.drawString(50, 800, "📄 Rapport de Dimensionnement 4G LTE - Zone : " + data["Zone"])
    y = 760
    for cle, valeur in data.items():
        c.drawString(50, y, f"{cle} : {valeur}")
        y -= 20

    c.drawImage("output/carte_couverture.png", 100, 300, width=350, height=200)
    c.save()
