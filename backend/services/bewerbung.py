import os
import uuid
import openai
from utils.pdf_exporter import generate_pdf, generate_docx

# Professioneller Systemprompt zur Bewerbungserstellung
SYSTEM_PROMPT = (
    """Du bist ein hochqualifizierter Bewerbungscoach mit langjähriger Erfahrung
in HR, Recruiting und Personalentwicklung. Deine Aufgabe ist es, auf Basis
der Stellenbeschreibung und Bewerberinformationen ein einzigartiges,
überzeugendes Bewerbungsschreiben zu erstellen.

Das Schreiben muss:
- Individuell und nicht generisch sein
- Einen starken Einstieg haben
- Konkrete Erfolge oder Erfahrungen hervorheben (wenn vorhanden)
- Authentisch und menschlich klingen, nicht wie eine KI-Formulierung
- ATS-optimiert sein mit relevanten Schlüsselwörtern
- Professionelle Sprache und klare Struktur haben (Einleitung, Hauptteil, Schluss)
- Eine überzeugende Abschlussformulierung enthalten

Vermeide überoptimierte Floskeln. Nutze stattdessen natürliche, überzeugende Sprache
mit klarem Bezug zur Stelle und Person."""
)


def validate_input(data: dict):
    """Validiert die Eingabedaten für die Bewerbungserstellung."""
    required_fields = ['job_title', 'job_description', 'user_info']
    for field in required_fields:
        if field not in data or not data[field].strip():
            raise ValueError(f"❌ Fehlender oder leerer Parameter: {field}")


def generate_bewerbung(data: dict):
    """
    Erstellt ein Bewerbungsschreiben basierend auf Jobdaten und Userinfo.
    Gibt den Bewerbungstext sowie die Pfade zu PDF & DOCX zurück.
    """
    validate_input(data)

    prompt = (
        f"Erstelle ein professionelles, individuelles Bewerbungsschreiben für die Position \"{data['job_title']}\"."
        f"\n\n🔹 **Stellenbeschreibung:**\n{data['job_description']}"
        f"\n\n🔹 **Bewerberprofil:**\n{data['user_info']}"
        "\n\nBitte schreibe überzeugend, strukturiert und passend zur Zielposition."
        " Kein generischer Einheitsbrei. Der Stil soll motiviert, kompetent und selbstbewusst wirken."
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
    pdf_filename = generate_pdf(result, "bewerbung")
    docx_filename = generate_docx(result, "bewerbung")

    return result, f"/static/{pdf_filename}", f"/static/{docx_filename}"

