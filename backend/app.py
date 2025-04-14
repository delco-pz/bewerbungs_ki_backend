import os
import logging
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

from services.bewerbung import generate_bewerbung
from services.lebenslauf import generate_lebenslauf

# Initialisierung
load_dotenv()
app = Flask(__name__)
CORS(app)
os.makedirs("static", exist_ok=True)

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API-Key Prüfen
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logger.critical("❌ OPENAI_API_KEY fehlt in .env")
    raise RuntimeError("OPENAI_API_KEY ist nicht gesetzt.")

# Bewerbung generieren
@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    logger.info("🔹 Anfrage erhalten für Bewerbung")

    try:
        result, pdf_url, docx_url = generate_bewerbung(data)
        return jsonify({
            "text": result,
            "pdf_url": pdf_url,
            "docx_url": docx_url
        }), 200

    except ValueError as ve:
        logger.warning(f"⚠️ Ungültige Eingabe: {ve}")
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        logger.error(f"❌ Fehler bei Bewerbung: {e}", exc_info=True)
        return jsonify({"error": "Interner Serverfehler"}), 500

# Lebenslauf generieren
@app.route("/generate_cv", methods=["POST"])
def generate_cv():
    data = request.get_json()
    logger.info("🔹 Anfrage erhalten für Lebenslauf")

    try:
        result, pdf_url, docx_url = generate_lebenslauf(data)
        return jsonify({
            "text": result,
            "pdf_url": pdf_url,
            "docx_url": docx_url
        }), 200

    except ValueError as ve:
        logger.warning(f"⚠️ Ungültige Eingabe: {ve}")
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        logger.error(f"❌ Fehler bei Lebenslauf: {e}", exc_info=True)
        return jsonify({"error": "Interner Serverfehler"}), 500

# Generierte Dateien bereitstellen
@app.route("/static/<path:filename>")
def serve_static(filename):
    return send_from_directory("static", filename)

# App starten
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug_mode)

