import os
import logging
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

# Eigene Services
from services.bewerbung import generate_bewerbung
from services.lebenslauf import generate_lebenslauf

# 🔧 Initialisierung
load_dotenv()
app = Flask(__name__)

from flask_cors import cross_origin
# 📁 Sicherstellen, dass statisches Verzeichnis existiert
os.makedirs("static", exist_ok=True)

# 🧾 Logging aktivieren
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 🔑 OpenAI-API-Key prüfen
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logger.critical("❌ OPENAI_API_KEY fehlt in .env")
    raise RuntimeError("OPENAI_API_KEY ist nicht gesetzt.")

# 🔽 Bewerbung generieren
@app.route("/generate", methods=["POST"])
@cross_origin(origin="https://ai-creation-of-cv-resume.webflow.io")
def generate():
    
    data = request.get_json()
    logger.info("📩 Bewerbung: Anfrage erhalten")

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

# 📄 Lebenslauf generieren
@app.route("/generate_cv", methods=["POST"])
@cross_origin(origin="https://ai-creation-of-cv-resume.webflow.io")
def generate_cv():
        
    data = request.get_json()
    logger.info("📄 Lebenslauf: Anfrage erhalten")

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

# 📦 Generierte Dateien ausliefern
@app.route("/static/<path:filename>")
def serve_static(filename):
    return send_from_directory("static", filename)

# 🚀 App starten
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    debug_mode = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    logger.info(f"🚀 Server läuft auf Port {port} | Debug: {debug_mode}")
    app.run(host="0.0.0.0", port=port, debug=debug_mode)

