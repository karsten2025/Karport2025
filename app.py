import os
from flask import (
    Flask,
    render_template,
    request,
    g,
    jsonify,
    redirect,
    make_response,
)

CLIENT_PORTAL = "https://client-portal-4wir.onrender.com"


app = Flask(__name__)


# --- Dieser Block bleibt unverändert ---
@app.before_request
def detect_language():
    g.lang = request.args.get("lang", "de")


@app.context_processor
def inject_language():
    return dict(lang=g.lang)


# --- Dieser Block bleibt unverändert ---
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/load/<section>")
def load_section(section):
    try:
        template_name = f"partials/{section}.{g.lang}.html"
        return render_template(template_name)
    except Exception as e:
        print(f"Error loading template: {e}")
        return "Inhalt nicht gefunden.", 404


@app.route("/certificates/<category>")
def list_certificates(category):
    try:
        dir_path = os.path.join(app.static_folder, "certificates", category)
        if os.path.isdir(dir_path):
            all_files = sorted(os.listdir(dir_path), reverse=True)
            return jsonify(all_files)
    except Exception as e:
        print(f"Error listing certificates: {e}")
    return jsonify([])


@app.route("/explore")
def go_explore():
    lang = request.args.get("lang", "de")
    return redirect(f"{CLIENT_PORTAL}/explore?lang={lang}", code=302)


@app.route("/brief")
def go_brief():
    lang = request.args.get("lang", "de")
    return redirect(f"{CLIENT_PORTAL}/brief?lang={lang}", code=302)


@app.route("/offer")
def go_offer():
    lang = request.args.get("lang", "de")
    return redirect(f"{CLIENT_PORTAL}/offer?lang={lang}", code=302)


@app.route("/portal")
def go_portal():
    return redirect(f"{CLIENT_PORTAL}/portal", code=302)


# 👉 NEU: Impressum & Datenschutz
@app.route("/impressum")
def impressum():
    return render_template("partials/impressum.de.html")


@app.route("/datenschutz")
def datenschutz():
    return render_template("partials/datenschutz.de.html")

@app.route("/donate")
def donate():
    lang = request.args.get("lang", "de")
    if lang not in ("de", "en"):
        lang = "de"
    return render_template("donate.html", lang=lang)


@app.route("/sitemap.xml")
def sitemap():
    """Erzeugt die sitemap.xml."""
    sitemap_xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="https://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://zenk-pm-now.de/</loc>
    <lastmod>2025-11-11</lastmod> 
    <changefreq>monthly</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>"""

    response = make_response(sitemap_xml_content)
    response.headers["Content-Type"] = "application/xml"
    return response


if __name__ == "__main__":
    app.run(debug=True)
