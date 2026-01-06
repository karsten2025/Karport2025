import os
from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    g,
    send_from_directory,
    make_response,
)
from dotenv import load_dotenv
from google import genai
from datetime import datetime  # NEU: Für die Zeitberechnung

# 1. KONFIGURATION & INITIALISIERUNG
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
CLIENT_PORTAL = "https://client-portal-4wir.onrender.com"

app = Flask(__name__)


# 2. SPRACH-LOGIK (Ihre Referenz)
@app.before_request
def detect_language():
    g.lang = request.args.get("lang", "de")


@app.context_processor
def inject_language():
    return dict(lang=g.lang)


# 3. HILFSFUNKTION KNOWLEDGE BASE
def load_karsten_knowledge(lang):
    try:
        filename = f"knowledge/karsten_base_{lang}.md"
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return "Knowledge base not found."


# 4. HAUPTROUTEN (Navigation)
@app.route("/")
def index():
    return render_template("index.html")


# 5. CHATBOT-ROUTE (Gemini 2.0 Flash - Optimiert für Ihr bezahltes Konto)
@app.route("/ask", methods=["POST"])
@app.route("/ask", methods=["POST"])
def ask_gemini():
    data = request.get_json()
    user_message = data.get("message")
    lang = data.get("lang", g.lang)

    # NEU: Aktuelles Datum formatieren
    today = datetime.now().strftime("%d. %B %Y")

    kb_content = load_karsten_knowledge(lang)

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            config={
                "system_instruction": (
                    f"Du bist der KI-Assistent von Karsten Zenk. Heute ist der {today}. "
                    f"Antworte strikt in der Sprache: {'Deutsch' if lang == 'de' else 'Englisch'}. "
                    f"Nutze dieses Wissen: {kb_content}. "
                    "Du darfst logische Berechnungen (wie das aktuelle Alter) basierend auf dem heutigen Datum durchführen. "
                    "Falls Informationen fehlen, verweise auf Karsten Zenk persönlich."
                )
            },
            contents=user_message,
        )
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"reply": f"API-Fehler: {str(e)}"}), 500


# 6. AKKORDEON-LOGIK (Ihre Referenz - Repariert)
@app.route("/certificates/<category>")
def list_certificates(category):
    try:
        # Greift exakt auf Ihren static-Ordner zu
        dir_path = os.path.join(app.static_folder, "certificates", category)
        if os.path.isdir(dir_path):
            all_files = sorted(os.listdir(dir_path), reverse=True)
            return jsonify(all_files)
    except Exception as e:
        print(f"Error listing certificates: {e}")
    return jsonify([])


# 7. RECHTLICHES (Ihre Referenz - Pfade zu den Partials)
@app.route("/impressum")
def impressum():
    return render_template("partials/impressum.de.html")


@app.route("/datenschutz")
def datenschutz():
    return render_template("partials/datenschutz.de.html")


# 8. SPENDEN-LOGIK (Ihre Referenz - PayPal-Funktionalität)
@app.route("/donate")
def donate():
    lang = request.args.get("lang", "de")
    if lang not in ("de", "en"):
        lang = "de"
    return render_template("donate.html", lang=lang)


@app.route("/donate/thanks")
def donate_thanks():
    lang = request.args.get("lang", "de")
    if lang not in ("de", "en"):
        lang = "de"
    return render_template("donate_thanks.html", lang=lang)


# 9. SYSTEM-ROUTEN & PORTAL-REDIRECTS
@app.route("/load/<section>")
def load_section(section):
    try:
        template_name = f"partials/{section}.{g.lang}.html"
        return render_template(template_name)
    except Exception as e:
        return "Inhalt nicht gefunden.", 404


@app.route("/explore")
@app.route("/brief")
@app.route("/offer")
def redirects():
    path = request.path.strip("/")
    return redirect(f"{CLIENT_PORTAL}/{path}?lang={g.lang}")


@app.route("/robots.txt")
def robots_txt():
    return send_from_directory(app.root_path, "robots.txt", mimetype="text/plain")


@app.route("/sitemap.xml")
def sitemap():
    sitemap_xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="https://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://zenk-pm-now.de/</loc></url>
</urlset>"""
    response = make_response(sitemap_xml_content)
    response.headers["Content-Type"] = "application/xml"
    return response


# 10. SERVER START (Fix für macOS)
if __name__ == "__main__":
    # use_reloader=False verhindert den OSError [Errno 38] auf Ihrem Mac
    app.run(debug=True, port=5000, use_reloader=False)
