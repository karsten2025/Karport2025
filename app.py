import os
from flask import Flask, render_template, request, g, jsonify

app = Flask(__name__)

# --- Dieser Block bleibt unverändert ---
@app.before_request
def detect_language():
    g.lang = request.args.get('lang', 'de')

@app.context_processor
def inject_language():
    return dict(lang=g.lang)

# --- Dieser Block bleibt unverändert ---
@app.route('/')
def index():
    return render_template('index.html')

# --- Dieser Block bleibt unverändert ---
@app.route('/load/<section>')
def load_section(section):
    try:
        template_name = f"partials/{section}.{g.lang}.html"
        return render_template(template_name)
    except Exception as e:
        print(f"Error loading template: {e}")
        return "Inhalt nicht gefunden.", 404

# --- ÜBERARBEITETE FUNKTION: Liste der statischen Dateien holen ---
# HINWEIS: Diese Funktion holt jetzt wieder ALLE Dateien.
@app.route('/certificates/<category>')
def list_certificates(category):
    try:
        dir_path = os.path.join(app.static_folder, "certificates", category)
        if os.path.isdir(dir_path):
            all_files = sorted(os.listdir(dir_path), reverse=True)
            # KORREKTUR: Das Limit wurde entfernt.
            return jsonify(all_files)
    except Exception as e:
        print(f"Error listing certificates: {e}")
    return jsonify([])

# --- Dieser Block bleibt unverändert ---
if __name__ == '__main__':
    app.run(debug=True)
