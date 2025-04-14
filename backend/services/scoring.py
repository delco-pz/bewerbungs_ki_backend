# 🔍 Erste Scoring-Logik – ideal für Freemium-Angebot & Bewertung

def score_application(text: str) -> dict:
    # Später: OpenAI-Scoring oder Fine-Tuned Model
    score = {
        "totalScore": 83,
        "categories": [
            {"title": "Struktur", "score": 21},
            {"title": "Relevanz zur Stelle", "score": 22},
            {"title": "Sprache & Tonalität", "score": 19},
            {"title": "Persönlichkeit", "score": 21}
        ],
        "overallFeedback": (
            "Die Bewerbung ist gut strukturiert, geht auf relevante Anforderungen ein "
            "und bringt eine authentische Motivation rüber. Im Sprachstil gibt es kleine Schwächen – "
            "hier wäre etwas mehr Persönlichkeit wünschenswert."
        )
    }
    return score
