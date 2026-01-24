import os
import glob
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
from datetime import datetime
from langdetect import detect, LangDetectException

# 1. KONFIGURATION & INITIALISIERUNG
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
CLIENT_PORTAL = "https://client-portal-4wir.onrender.com"

app = Flask(__name__)


# 2. SPRACH-LOGIK
@app.before_request
def set_global_lang():
    """Setzt g.lang aus URL-Parameter für Template-Rendering"""
    g.lang = request.args.get("lang", "de")


@app.context_processor
def inject_language():
    return dict(lang=g.lang)


# 3. HILFSFUNKTIONEN

def detect_language(text):
    """
    Erkennt automatisch die Sprache einer Benutzernachricht.
    Verwendet Keyword-Matching für Zuverlässigkeit bei kurzen Texten.
    Gibt 'de' oder 'en' zurück, Fallback auf 'de'.
    """
    text_lower = text.lower()
    
    # Englische Keywords (häufige Fragewörter und Verben)
    en_keywords = ['how', 'what', 'when', 'where', 'who', 'why', 'which', 
                   'can', 'could', 'would', 'should', 'do', 'does', 'did',
                   'is', 'are', 'was', 'were', 'have', 'has', 'had',
                   'tell', 'show', 'explain', 'describe', 'his', 'her', 'their']
    
    # Deutsche Keywords (häufige Fragewörter und Verben)
    de_keywords = ['wie', 'was', 'wann', 'wo', 'wer', 'warum', 'welche', 'welcher', 'welches',
                   'kannst', 'könntest', 'würdest', 'solltest', 'bist', 'sind', 'war', 'waren',
                   'hast', 'hat', 'hatte', 'hatten', 'sage', 'zeige', 'erkläre', 'beschreibe',
                   'sein', 'seine', 'ihrer', 'seinem']
    
    # Zähle Keyword-Treffer
    en_count = sum(1 for keyword in en_keywords if f' {keyword} ' in f' {text_lower} ' or text_lower.startswith(keyword + ' '))
    de_count = sum(1 for keyword in de_keywords if f' {keyword} ' in f' {text_lower} ' or text_lower.startswith(keyword + ' '))
    
    # Wenn Keyword-Matching eindeutig ist
    if en_count > de_count:
        return 'en'
    elif de_count > en_count:
        return 'de'
    
    # Fallback: langdetect
    try:
        detected = detect(text)
        if detected == 'de':
            return 'de'
        elif detected in ['en', 'nl', 'da', 'no', 'sv', 'af']:  # Englisch und verwandte
            return 'en'
        else:
            return 'de'
    except LangDetectException:
        return 'de'


def load_karsten_knowledge(lang):
    """
    Lädt alle Markdown-Dateien aus knowledge_base_final für die gewählte Sprache.
    Kombiniert sie zu einem großen Kontext für den Chatbot.
    """
    try:
        # Lade alle Dateien für die gewählte Sprache
        pattern = f"knowledge_base_final/*_{lang}.md"
        files = sorted(glob.glob(pattern))
        
        if not files:
            # Fallback auf alte Dateien, falls knowledge_base_final leer ist
        filename = f"knowledge/karsten_base_{lang}.md"
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()
        
        # Kombiniere alle Dateien
        combined_content = []
        combined_content.append(f"# Karsten Zenk - Vollständige Wissensdatenbank ({lang.upper()})\n")
        combined_content.append(f"Generiert aus {len(files)} Dokumenten\n\n")
        
        for filepath in files:
            filename = os.path.basename(filepath)
            doc_name = filename.replace(f"_{lang}.md", "")
            
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read().strip()
                
            if content:  # Nur nicht-leere Dateien hinzufügen
                combined_content.append(f"\n## Dokument: {doc_name}\n")
                combined_content.append(content)
                combined_content.append("\n---\n")
        
        return "\n".join(combined_content)
        
    except Exception as e:
        print(f"Fehler beim Laden der Knowledge Base: {e}")
        return "Knowledge base could not be loaded."


# 4. HAUPTROUTEN (Navigation)
@app.route("/")
def index():
    return render_template("index.html")


# 5. CHATBOT-ROUTE (Gemini 2.0 Flash mit intelligenter Spracherkennung)
@app.route("/ask", methods=["POST"])
def ask_gemini():
    data = request.get_json()
    user_message = data.get("message")
    frontend_lang = data.get("lang", g.lang)  # Sprache aus dem Frontend
    
    # 🎯 INTELLIGENTE SPRACHERKENNUNG
    # Erkenne die Sprache der Benutzernachricht automatisch
    detected_lang = detect_language(user_message)
    
    # Verwende die erkannte Sprache (nicht die Frontend-Sprache!)
    lang = detected_lang

    # NEU: Aktuelles Datum formatieren
    today = datetime.now().strftime("%d. %B %Y")

    # Lade die Knowledge Base in der erkannten Sprache
    kb_content = load_karsten_knowledge(lang)
    
    # ULTRA-EXPLIZITE Sprachanweisung mit mehrfacher Betonung
    if lang == 'de':
        system_prompt = f"""Du bist Karstens KI-Assistent. Heute ist der {today}.

SPRACHE: Du MUSST in DEUTSCHER Sprache antworten!
- Jedes Wort muss auf Deutsch sein
- Keine englischen Begriffe verwenden
- 100% deutschsprachige Antwort

Wissensgrundlage:
{kb_content}

Regeln:
- Berechne das Alter basierend auf dem heutigen Datum
- Bei fehlenden Infos: Verweise auf Karsten Zenk persönlich
- WICHTIG: Antworte NUR auf Deutsch!"""

        user_prompt = f"""DEUTSCH: {user_message}

Antworte ausschließlich auf Deutsch!"""
        
    else:
        system_prompt = f"""You are Karsten's AI assistant. Today is {today}.

LANGUAGE: You MUST respond in ENGLISH!
- Every word must be in English
- Do not use any German terms
- 100% English language response

Knowledge base:
{kb_content}

Rules:
- Calculate age based on today's date
- If info is missing: Refer to Karsten Zenk personally
- IMPORTANT: Respond ONLY in English!"""

        user_prompt = f"""ENGLISH: {user_message}

Respond exclusively in English!"""

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            config={
                "system_instruction": system_prompt
            },
            contents=user_prompt,
        )
        
        # Gib auch die erkannte Sprache zurück (für Debugging/Feedback)
        return jsonify({
            "reply": response.text,
            "detected_language": lang,
            "frontend_language": frontend_lang
        })
        
    except Exception as e:
        return jsonify({
            "reply": f"API-Fehler: {str(e)}",
            "detected_language": lang
        }), 500


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
