import os
import glob
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from PIL import Image
import subprocess
import shutil

# Umgebungsvariablen laden (.env Datei)
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# KONFIGURATION
INPUT_DIR = "./inputs"  # Ordner mit deinen PDFs, JPGs, PNGs
OUTPUT_DIR = "./knowledge_base_final"
MODELS = ["gpt-4o"] # Wir nutzen GPT-4o für beste Qualität

def image_to_pdf(image_path):
    """Bilder temporär in PDF wandeln, da Marker für Dokument-Layouts optimiert ist."""
    pdf_path = image_path.with_suffix(".temp.pdf")
    img = Image.open(image_path).convert('RGB')
    img.save(pdf_path, "PDF", resolution=100.0)
    return pdf_path

# --- OPTIMIERT FÜR GPT-5.2 ---
def translate_markdown(text, target_lang):
    print(f"  -> Nutze GPT-5.2 für Übersetzung ({target_lang})...")
    
    # In der GPT-5 Ära nutzen wir oft den 'developer' oder 'user' prompt
    # für präzise Anweisungen.
    prompt = f"""
    Du bist ein Experte für Projektmanagement-Zertifizierungen,Geschäftsprozessmanagement, Complex adaptive systems, Konstruktivismus und Systemtheorie, Ökonomie, Betriebswirtschaft,General Semantics,Zen-Buddhismus,Taoismus und Karriere-Consulting.
    Übersetze den folgenden Markdown-Inhalt für die Webseite 'zenk-pm-now.de' ins {target_lang}.
    
    ANWEISUNGEN:
    1. Behalte die Markdown-Struktur (Tabellen, Fettdruck, Header) exakt bei.
    2. Nutze korrekte Fachterminologie (z.B. PMP, Projektlebenszyklus, Stakeholder,etc.).
    3. Der Ton soll professionell und vertrauenserweckend sein.
    4. Gib nur den übersetzten Text zurück.
    
    TEXT:
    {text}
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-5.2", # Hier kannst du auch "gpt-5.2-pro" nutzen
            messages=[
                {"role": "user", "content": prompt}
            ],
            # GPT-5 Modelle managen ihre Temperatur oft selbst, 
            # aber wir können die Präzision hier forcieren:
            prediction={"type": "content"} if "gpt-5" in "gpt-5.2" else None 
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Fehler bei der GPT-5.2 Übersetzung: {e}")
        return text

def run_pipeline():
    # 1. Setup
    print("Starte Verarbeitung der Dokumente...")
    Path(OUTPUT_DIR).mkdir(exist_ok=True)
    
    # Erstelle ein temporäres Ausgabeverzeichnis für Marker
    temp_output = "./temp_markdown"
    Path(temp_output).mkdir(exist_ok=True)
    
    # Führe marker über das gesamte Verzeichnis aus
    print("\n=== Schritt 1: Extrahiere Text mit marker-pdf ===")
    result = subprocess.run(
        ["marker", INPUT_DIR, "--output_format", "markdown", "--disable_multiprocessing"],
        capture_output=True,
        text=True,
        cwd="."
    )
    
    # Marker speichert Ausgaben im {INPUT_DIR}_out Ordner
    marker_output_dir = Path(f"{INPUT_DIR}_out")
    
    if not marker_output_dir.exists():
        print(f"Fehler: Marker Output-Verzeichnis {marker_output_dir} existiert nicht")
        print(f"stdout: {result.stdout}")
        print(f"stderr: {result.stderr}")
        return
    
    print(f"\n=== Schritt 2: Übersetze Markdown-Dateien ===")
    
    # Verarbeite alle generierten Markdown-Dateien
    for md_file in marker_output_dir.glob("*.md"):
        print(f"\nVerarbeite: {md_file.name}")
        
        try:
            with open(md_file, "r", encoding="utf-8") as f:
                full_text = f.read()
            
            # Erstelle zweisprachige Versionen
            for lang_code, lang_name in [("de", "Deutsch"), ("en", "Englisch")]:
                print(f"  -> Übersetze nach {lang_name}...")
                translated_content = translate_markdown(full_text, lang_name)
                
                output_file = Path(OUTPUT_DIR) / f"{md_file.stem}_{lang_code}.md"
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(translated_content)
                print(f"  [Erledigt] {output_file.name}")
        
        except Exception as e:
            print(f"  [Fehler] {e}")
    
    print("\n=== Fertig! ===")
    print(f"Ausgabe in: {OUTPUT_DIR}")

if __name__ == "__main__":
    run_pipeline()