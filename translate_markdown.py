import os
import glob
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# Umgebungsvariablen laden
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# KONFIGURATION
INPUT_DIR = "./inputs_out"
OUTPUT_DIR = "./knowledge_base_final"

def translate_markdown(text, target_lang):
    """Übersetzt Markdown-Inhalt mit GPT-5.2"""
    print(f"  -> Nutze GPT-5.2 für Übersetzung ({target_lang})...")
    
    prompt = f"""
    Du bist ein Experte für Projektmanagement-Zertifizierungen, Geschäftsprozessmanagement, Complex adaptive systems, Konstruktivismus und Systemtheorie, Ökonomie, Betriebswirtschaft, General Semantics, Zen-Buddhismus, Taoismus und Karriere-Consulting.
    Übersetze den folgenden Markdown-Inhalt für die Webseite 'zenk-pm-now.de' ins {target_lang}.
    
    ANWEISUNGEN:
    1. Behalte die Markdown-Struktur (Tabellen, Fettdruck, Header) exakt bei.
    2. Nutze korrekte Fachterminologie (z.B. PMP, Projektlebenszyklus, Stakeholder, etc.).
    3. Der Ton soll professionell und vertrauenserweckend sein.
    4. Gib nur den übersetzten Text zurück.
    
    TEXT:
    {text}
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-5.2",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"    [Fehler] {e}")
        return text

def main():
    print("=" * 60)
    print("MARKDOWN-ÜBERSETZUNG MIT GPT-5.2")
    print("=" * 60)
    
    # Erstelle Output-Verzeichnis
    Path(OUTPUT_DIR).mkdir(exist_ok=True)
    
    # Hole alle Markdown-Dateien
    md_files = glob.glob(os.path.join(INPUT_DIR, "*.md"))
    total = len(md_files)
    
    print(f"\nGefunden: {total} Markdown-Dateien")
    print(f"Ziel: {total * 2} zweisprachige Dateien\n")
    
    for idx, md_file in enumerate(md_files, 1):
        md_path = Path(md_file)
        print(f"\n[{idx}/{total}] Verarbeite: {md_path.name}")
        
        try:
            # Lade Markdown
            with open(md_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Überspringe leere Dateien
            if len(content.strip()) < 10:
                print("  [Übersprungen] Datei zu kurz")
                continue
            
            # Erstelle zweisprachige Versionen
            for lang_code, lang_name in [("de", "Deutsch"), ("en", "Englisch")]:
                output_file = Path(OUTPUT_DIR) / f"{md_path.stem}_{lang_code}.md"
                
                # Überspringe bereits existierende Dateien
                if output_file.exists():
                    print(f"  [Übersprungen] {output_file.name} existiert bereits")
                    continue
                
                print(f"  -> Übersetze nach {lang_name}...")
                translated = translate_markdown(content, lang_name)
                
                # Speichere
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(translated)
                print(f"  ✓ Gespeichert: {output_file.name}")
        
        except Exception as e:
            print(f"  [Fehler] {e}")
    
    print("\n" + "=" * 60)
    print("FERTIG!")
    final_count = len(list(Path(OUTPUT_DIR).glob("*.md")))
    print(f"Erstellt: {final_count} Dateien in {OUTPUT_DIR}")
    print("=" * 60)

if __name__ == "__main__":
    main()


