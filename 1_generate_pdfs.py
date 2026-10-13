"""
Step 1 - Create 10 travel guide PDFs (5 pages each) in data/pdfs/.

Run:  .venv\\Scripts\\python.exe 1_generate_pdfs.py
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak

import config
from city_content import CITIES

styles = getSampleStyleSheet()
TITLE = ParagraphStyle("title", parent=styles["Title"], fontSize=26, spaceAfter=6)
SUBTITLE = ParagraphStyle("subtitle", parent=styles["Italic"], fontSize=13, alignment=1, spaceAfter=18)
HEADING = ParagraphStyle("heading", parent=styles["Heading1"], fontSize=18, spaceAfter=12)
BODY = ParagraphStyle("body", parent=styles["BodyText"], fontSize=11.5, leading=17, spaceAfter=10)


def make_footer(city):
    def footer(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 9)
        canvas.drawString(2 * cm, 1.2 * cm, f"{city} Travel Guide - educational demo content")
        canvas.drawRightString(A4[0] - 2 * cm, 1.2 * cm, f"Page {doc.page} of 5")
        canvas.restoreState()
    return footer


def build_pdf(city, info):
    path = config.PDF_DIR / f"{city.replace(' ', '_')}_Travel_Guide.pdf"
    doc = SimpleDocTemplate(str(path), pagesize=A4, title=f"{city} Travel Guide",
                            leftMargin=2.2 * cm, rightMargin=2.2 * cm, topMargin=2 * cm, bottomMargin=2 * cm)
    story = [Paragraph(f"{city} Travel Guide", TITLE),
             Paragraph(f"{info['tagline']} - {info['country']}", SUBTITLE)]

    for i, (section_title, paragraphs) in enumerate(info["sections"]):
        if i > 0:
            story.append(PageBreak())          # one section = one page
        # The city name is repeated in every heading so each page makes sense on its own
        story.append(Paragraph(f"{city}: {section_title}", HEADING))
        story += [Paragraph(p, BODY) for p in paragraphs]
        story.append(Spacer(1, 6))

    footer = make_footer(city)
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    return path


if __name__ == "__main__":
    config.PDF_DIR.mkdir(parents=True, exist_ok=True)
    for city, info in CITIES.items():
        print("Created", build_pdf(city, info).name)
