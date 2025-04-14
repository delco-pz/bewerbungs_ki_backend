from utils.cv_pdf_styles import generate_random_cv_pdf
import os
import uuid
import openai
from utils.pdf_exporter import generate_pdf, generate_docx

# System-Prompt für Lebenslauf-Generierung
SYSTEM_PROMPT = (
    "Du bist ein professioneller Karriereberater mit Spezialisierung auf das Erstellen von individuellen, klar strukturierten und "
    "zielgerichteten Lebensläufen. Dein Ziel ist es, für den Nutzer einen Lebenslauf zu generieren, der:"
    "\n- Übersichtlich ist"
    "\n- Klar priorisiert (neueste Erfahrung zuerst)"
    "\n- Fachlich überzeugt"
    "\n- Sofort lesbar und strukturiert wirkt"
    "\n- ATS-optimiert ist"
    "\n\nDer Stil soll professionell, aber natürlich sein."
)

def validate_input(data: dict):
    """Validiert die Eingabedaten für den Lebenslauf."""
    required_fields = ["name", "contact", "experience", "education", "skills"]
    for field in required_fields:
        if field not in data or not data[field].strip():
            raise ValueError(f"❌ Fehlender oder leerer Parameter: {field}")

def generate_lebenslauf(data: dict):
    """
    Erstellt einen strukturierten, individuellen Lebenslauf.
    Gibt den Text sowie Pfade zu PDF & DOCX zurück.
    """
    validate_input(data)

    prompt = (
        f"Erstelle einen professionellen Lebenslauf für {data['name']}.\n"
        f"\n📧 **Kontakt:** {data['contact']}"
        f"\n\n💼 **Berufserfahrung:**\n{data['experience']}"
        f"\n\n🎓 **Ausbildung:**\n{data['education']}"
        f"\n\n🛠 **Fähigkeiten:**\n{data['skills']}"
        "\n\nBitte formuliere überzeugend, klar und in professioneller Sprache."
    )

    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1500
    )

    result = response.choices[0].message.content
    pdf_filename = generate_random_cv_pdf({
        'name': data['name'],
        'contact': data['contact'],
        'sections': {
            'Ausbildung': data['education'].split('\n'),
            'Berufserfahrung': data['experience'].split('\n'),
        'Kenntnisse': data['skills'].split('\n'),
        }
    })
    
    pdf_filename = generate_random_cv_pdf({
        'name': data['name'],
        'contact': data['contact'],
        'sections': {
            'Ausbildung': data['education'].split('\n'),
            'Berufserfahrung': data['experience'].split('\n'),
            'Kenntnisse': data['skills'].split('\n'),
        }
    })

    docx_filename = generate_docx(result, "cv")

    return result, f"/static/{pdf_filename}", f"/static/{docx_filename}"

