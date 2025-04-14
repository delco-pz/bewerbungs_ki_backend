import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# 🧠 Systemrolle – langfristig erweiterbar mit Presets
APPLICATION_SYSTEM_PROMPT = """
Du bist ein erfahrener Bewerbungscoach & HR-Profi. Dein Ziel:
Perfekte, authentische, auf die Stelle zugeschnittene Anschreiben.
"""

CV_SYSTEM_PROMPT = "Du bist ein Top-HR-Berater. Dein Ziel: Moderne, klare und starke Lebensläufe."

# 📌 Bewerbungsgenerator
def generate_application_letter(job_title: str, job_description: str, user_info: str, tone: str = "professionell & persönlich") -> str:
    prompt = f"""
Erstelle ein überzeugendes Bewerbungsschreiben für **{job_title}** mit folgendem Stil: _{tone}_.

🔹 **Stellenbeschreibung:**
{job_description}

🔹 **Bewerber-Info:**
{user_info}

🔸 Regeln:
- Kein generischer Einstieg – beginne mit einem **Erfolg oder starkem Aufhänger**
- Verwende eine **natürliche, authentische Sprache**, kein typisches KI-Pattern
- Beziehe dich **direkt auf das Unternehmen**
- Kombiniere **fachliche Kompetenz + persönliche Motivation**
- Abschließen mit **konkretem Gesprächsangebot**, nicht Floskeln
"""

    response = openai.OpenAI().chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": APPLICATION_SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        temperature=0.65,
        max_tokens=1500
    )
    return response.choices[0].message.content.strip()

# 📌 Lebenslaufgenerator
def generate_cv_text(name: str, contact: str, experience: str, education: str, skills: str, target_role: str = "") -> str:
    prompt = f"""
Erstelle einen modernen, prägnanten Lebenslauf für **{name}**.

🎯 Zielrolle: {target_role if target_role else "nicht angegeben"}

📞 Kontakt:
{contact}

💼 Berufserfahrung:
{experience}

🎓 Ausbildung:
{education}

🛠 Fähigkeiten:
{skills}

🧠 Hinweise:
- Struktur: Berufserfahrung zuerst, dann Ausbildung, dann Skills
- Verwende Bullet-Points, keine Romane
- Hebe konkrete Erfolge hervor, wenn vorhanden
- Keine generischen Soft Skills ohne Kontext
- Wenn keine Zahlen vorhanden, beschreibe Wirkung & Verantwortungsbereich
"""

    response = openai.OpenAI().chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": CV_SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        temperature=0.6,
        max_tokens=1500
    )
    return response.choices[0].message.content.strip()
