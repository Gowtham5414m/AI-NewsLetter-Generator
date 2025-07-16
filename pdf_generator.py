from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime

def create_newsletter_pdf(articles, category="General"):
    filename = f"Newsletter_{category}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    c = canvas.Canvas(filename, pagesize=A4)

    width, height = A4
    y = height - 50

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, f"{category} News - {datetime.now().strftime('%Y-%m-%d')}")
    y -= 30

    c.setFont("Helvetica", 12)

    for i, article in enumerate(articles, start=1):
        title = f"{i}. {article['title']}"
        url = article['url']

        if y < 100:
            c.showPage()
            y = height - 50
            c.setFont("Helvetica", 12)

        c.drawString(50, y, title)
        y -= 20
        c.setFont("Helvetica-Oblique", 10)
        c.drawString(60, y, url)
        y -= 30
        c.setFont("Helvetica", 12)

    c.save()
    return filename
