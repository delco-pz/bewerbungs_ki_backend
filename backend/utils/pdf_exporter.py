from fpdf import FPDF
from docx import Document
import uuid
import os
from datetime import datetime

FONT_FAMILY = "Arial"
FONT_SIZE = 12
MARGIN = 15
LINE_HEIGHT = 10

# 📄 PDF-Erstellung mit Kopf- und Fußzeile
class StyledPDF(FPDF):
    def header(self):
        self.set_font(FONT_FAMILY, 'B', 14)
        self.set_text_color(40, 40, 40)
        self.cell(0, 10, 'Bewerbungsunterlagen', ln=True, align='C')
        self.ln(5)
        self.set_draw_color(180, 180, 180)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font(FONT_FAMILY, 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'Seite {self.page_no()} | Generiert am {datetime.now().strftime("%d.%m.%Y")}', align='C')

    def add_content(self, text):
        self.set_font(FONT_FAMILY, '', FONT_SIZE)
        self.set_text_color(0, 0, 0)
        lines = text.split("\n")
        for line in lines:
            self.multi_cell(0, LINE_HEIGHT, line.strip())
            self.ln(0.5)


def generate_pdf(text, doc_type="bewerbung"):
    """Erzeugt eine optisch ansprechende PDF-Datei."""
    pdf = StyledPDF()
    pdf.set_auto_page_break(auto=True, margin=MARGIN)
    pdf.add_page()

    # UTF-8 absichern
    text = text.encode("latin-1", "replace").decode("latin-1")
    pdf.add_content(text)

    filename = f"{doc_type}_{uuid.uuid4().hex}.pdf"
    path = os.path.join("static", filename)
    pdf.output(path)
    return filename


def generate_docx(text, doc_type="bewerbung"):
    """Erzeugt ein formatiertes Word-Dokument (DOCX)."""
    doc = Document()
    style = doc.styles['Normal']
    font = style.font
    font.name = FONT_FAMILY
    font.size = 240  # 12 pt

    for paragraph in text.split("\n\n"):
        if paragraph.strip():
            doc.add_paragraph(paragraph.strip())

    filename = f"{doc_type}_{uuid.uuid4().hex}.docx"
    path = os.path.join("static", filename)
    doc.save(path)
    return filename
