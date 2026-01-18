#!/usr/bin/env python3
"""
Verarbeitet ein neues DOCX-Dokument und integriert es in die Knowledge Base.
Pipeline: DOCX → PDF → Marker → GPT-5.2 Translation → knowledge_base_final/
"""

import os
import subprocess
import glob
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Konfiguration
INPUT_DOCX = "./inputs/Lebenslauf_Karsten_Zenk-DE-knowledge base.docx"
TEMP_PDF = "./inputs_out/Lebenslauf_Karsten_Zenk-DE-knowledge_base.pdf"
OUTPUT_DIR = "./knowledge_base_final"

def convert_docx_to_pdf():
    """Konvertiert DOCX zu PDF mit python-docx und fpdf (falls LibreOffice fehlt)."""
    print("📄 Konvertiere DOCX → PDF...")
    
    # Erstelle inputs_out falls nicht vorhanden
    Path("./inputs_out").mkdir(exist_ok=True)
    
    # Versuch 1: LibreOffice (beste Qualität)
    try:
        subprocess.run([
            "soffice",
            "--headless",
            "--convert-to", "pdf",
            "--outdir", "./inputs_out",
            INPUT_DOCX
        ], check=True, timeout=30)
        
        # Prüfe mögliche Output-Namen
        possible_names = [
            "./inputs_out/Lebenslauf_Karsten_Zenk-DE-knowledge base.pdf",
            "./inputs_out/Lebenslauf_Karsten_Zenk-DE-knowledge_base.pdf",
        ]
        
        for name in possible_names:
            if os.path.exists(name):
                if name != TEMP_PDF:
                    os.rename(name, TEMP_PDF)
                print(f"✅ PDF erstellt (LibreOffice): {TEMP_PDF}")
                return True
        
        print("⚠️ LibreOffice-Output nicht gefunden. Nutze Marker direkt auf DOCX...")
        return "skip_pdf"
        
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        print(f"⚠️ LibreOffice nicht verfügbar: {e}")
        print("→ Nutze Marker direkt auf DOCX...")
        return "skip_pdf"
    except Exception as e:
        print(f"⚠️ Fehler bei LibreOffice: {e}")
        return "skip_pdf"

def run_marker_on_document(input_file):
    """Führt Marker auf dem Dokument aus (PDF oder DOCX)."""
    print(f"🔍 Starte Marker-Verarbeitung auf: {input_file}")
    
    # Erstelle Output-Verzeichnis
    Path("./inputs_out").mkdir(exist_ok=True)
    
    try:
        # Marker CLI auf einzelnes Dokument (neue Syntax)
        result = subprocess.run([
            "marker_single",
            input_file,
            "--output_dir", "./inputs_out",
            "--output_format", "markdown"
        ], capture_output=True, text=True, check=True)
        
        print("✅ Marker erfolgreich")
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Marker-Fehler: {e.stderr}")
        return False

def translate_with_gpt52(text, target_lang):
    """Übersetzt Markdown mit GPT-5.2."""
    lang_name = "Deutsch" if target_lang == "de" else "Englisch"
    
    prompt = f"""Du bist ein professioneller Übersetzer. Übersetze den folgenden Markdown-Text nach {lang_name}.

Regeln:
- Behalte die Markdown-Formatierung bei
- Übersetze alle Inhalte sorgfältig
- Bewahre technische Begriffe wo sinnvoll
- Nutze professionelle Sprache

Text:
{text}
"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-5.2",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"⚠️ Übersetzungsfehler ({lang_name}): {e}")
        return text

def process_translation_pipeline():
    """Übersetzt die Marker-Ausgabe und speichert in knowledge_base_final."""
    print("🌍 Starte Übersetzungen...")
    
    # Finde die von Marker generierte Markdown-Datei (auch in Unterordnern)
    md_files = []
    
    # Suche in inputs_out/ und allen Unterordnern
    for root, dirs, files in os.walk("./inputs_out"):
        for file in files:
            if file.endswith(".md") and not file.endswith("_meta.md"):
                md_files.append(os.path.join(root, file))
    
    if not md_files:
        print("❌ Keine Markdown-Datei von Marker gefunden!")
        return False
    
    # Nehme die neueste Datei
    source_md = max(md_files, key=os.path.getmtime)
    print(f"📝 Verarbeite: {source_md}")
    
    # Lese Original-Markdown
    with open(source_md, "r", encoding="utf-8") as f:
        original_content = f.read()
    
    # Übersetze in beide Sprachen
    Path(OUTPUT_DIR).mkdir(exist_ok=True)
    
    for lang_code, lang_name in [("de", "Deutsch"), ("en", "Englisch")]:
        print(f"  🔄 Übersetze nach {lang_name}...")
        
        translated_content = translate_with_gpt52(original_content, lang_code)
        
        output_file = Path(OUTPUT_DIR) / f"Lebenslauf_Karsten_Zenk_{lang_code}.md"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(translated_content)
        
        print(f"  ✅ Gespeichert: {output_file.name}")
    
    return True

def main():
    """Hauptprozess: DOCX → PDF → Marker → Translation → Knowledge Base"""
    print("=" * 60)
    print("🚀 Verarbeite neues Dokument für Knowledge Base")
    print("=" * 60)
    
    # Schritt 1: DOCX → PDF (oder direkt DOCX wenn LibreOffice fehlt)
    conversion_result = convert_docx_to_pdf()
    
    if conversion_result == "skip_pdf":
        # Nutze DOCX direkt
        input_for_marker = INPUT_DOCX
    elif conversion_result:
        # Nutze konvertiertes PDF
        input_for_marker = TEMP_PDF
    else:
        print("❌ Abbruch: Konvertierung fehlgeschlagen")
        return
    
    # Schritt 2: Marker auf Dokument
    if not run_marker_on_document(input_for_marker):
        print("❌ Abbruch: Marker-Verarbeitung fehlgeschlagen")
        return
    
    # Schritt 3: GPT-5.2 Übersetzung
    if not process_translation_pipeline():
        print("❌ Abbruch: Übersetzung fehlgeschlagen")
        return
    
    print("\n" + "=" * 60)
    print("🎉 ERFOLGREICH! Dokument ist in Knowledge Base integriert!")
    print("=" * 60)
    print("\n📌 Nächste Schritte:")
    print("  1. Flask läuft? → Automatisch aktiv! ✅")
    print("  2. Flask läuft nicht? → 'flask run' starten")
    print("  3. Git-Deployment? → Sag Bescheid für Push zu GitHub")

if __name__ == "__main__":
    main()
