from fpdf import FPDF
import uuid
import os
import random
from datetime import datetime

class BaseCV(FPDF):
    def header(self):
        pass

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'Seite {self.page_no()} | Generiert am {datetime.now().strftime("%d.%m.%Y")}', align='C')

class ClassicCV(BaseCV):
    def build(self, data):
        self.add_page()
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, data['name'], ln=True)

        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, data['contact'])

        for section, content in data['sections'].items():
            self.set_font('Arial', 'B', 14)
            self.cell(0, 10, section, ln=True)
            self.set_font('Arial', '', 12)
            for entry in content:
                self.multi_cell(0, 10, f"- {entry}")
            self.ln(3)

class ModernCV(BaseCV):
    def build(self, data):
        self.add_page()
        self.set_fill_color(30, 75, 120)
        self.rect(0, 0, 70, 300, 'F')

        self.set_xy(10, 20)
        self.set_text_color(255)
        self.set_font('Arial', 'B', 16)
        self.cell(50, 10, data['name'], ln=True)

        self.set_font('Arial', '', 12)
        self.multi_cell(50, 10, data['contact'])

        y_start = 20
        self.set_xy(80, y_start)
        self.set_text_color(0)
        for section, content in data['sections'].items():
            self.set_font('Arial', 'B', 14)
            self.cell(0, 10, section, ln=True)
            self.set_font('Arial', '', 12)
            for entry in content:
                self.multi_cell(0, 10, f"• {entry}")
            self.ln(3)


def generate_random_cv_pdf(data: dict):
    pdf_class = random.choice([ClassicCV, ModernCV])
    pdf = pdf_class()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.build(data)

    filename = f"cv_{uuid.uuid4().hex}.pdf"
    path = os.path.join("static", filename)
    pdf.output(path)
    return filename

