#!/usr/bin/env python3
"""
Script zum Hinzufügen strukturierter Text-Dateien zur Knowledge Base.
Übersetzt den Text in DE + EN und speichert als Markdown.

Usage:
    python3 add_text_to_kb.py <input.txt> [--prefix 0001] [--title "Custom Title"]
"""

import os
import sys
import re
from pathlib import Path
from dotenv import load_dotenv
from google import genai

# Lade .env
load_dotenv()

def detect_language(text: str) -> str:
    """Erkennt die Sprache des Texts (de/en)."""
    sample = text[:500].lower()
    
    # Deutsche Keywords
    de_keywords = ['und', 'der', 'die', 'das', 'ist', 'mit', 'für', 'auf', 'von', 'zu', 'durch']
    en_keywords = ['the', 'and', 'is', 'are', 'for', 'with', 'this', 'that', 'from', 'to', 'by']
    
    de_count = sum(1 for kw in de_keywords if f' {kw} ' in sample)
    en_count = sum(1 for kw in en_keywords if f' {kw} ' in sample)
    
    return 'de' if de_count > en_count else 'en'

def translate_to_german(text: str, client, model_name: str) -> str:
    """Übersetzt Text nach Deutsch."""
    prompt = f"""Du bist ein professioneller Übersetzer für strategisches PMO-Management.

AUFGABE: Übersetze den folgenden Text ins Deutsche.

REGELN:
1. Behalte die Markdown-Formatierung bei
2. Übersetze Fachbegriffe kontextgerecht
3. Behalte proprietäre Begriffe wie "Value Engine", "Impact Cycle" etc. ENGLISCH
4. Übersetze Kapitelüberschriften vollständig
5. Keine Erklärungen, nur die Übersetzung

TEXT:
{text}
"""
    
    response = client.models.generate_content(
        model=model_name,
        contents=prompt
    )
    return response.text.strip()

def translate_to_english(text: str, client, model_name: str) -> str:
    """Übersetzt Text nach Englisch."""
    prompt = f"""You are a professional translator for strategic PMO management.

TASK: Translate the following text into English.

RULES:
1. Preserve all Markdown formatting
2. Translate technical terms contextually
3. Keep proprietary terms like "Value Engine", "Impact Cycle" in ENGLISH
4. Translate chapter headings completely
5. No explanations, only the translation

TEXT:
{text}
"""
    
    response = client.models.generate_content(
        model=model_name,
        contents=prompt
    )
    return response.text.strip()

def convert_to_markdown(text: str, title: str) -> str:
    """Konvertiert strukturierten Text zu Markdown."""
    lines = text.split('\n')
    markdown = []
    
    for line in lines:
        # Überschriften erkennen (====, ----)
        if line.strip().startswith('===') or line.strip().startswith('---'):
            continue
        
        # KAPITEL → ## Überschrift
        if line.strip().startswith('KAPITEL'):
            markdown.append(f"\n## {line.strip()}")
            continue
        
        # ALL CAPS Zeilen → ### Unterüberschrift
        if line.strip() and line.strip().isupper() and len(line.strip()) > 5:
            markdown.append(f"\n### {line.strip()}")
            continue
        
        # Normale Zeilen
        markdown.append(line)
    
    # Titel hinzufügen
    result = f"# {title}\n\n" + '\n'.join(markdown)
    return result

def save_to_knowledge_base(text_de: str, text_en: str, prefix: str, base_name: str):
    """Speichert DE + EN Versionen in knowledge_base_final/."""
    kb_dir = Path(__file__).parent / "knowledge_base_final"
    kb_dir.mkdir(exist_ok=True)
    
    # Dateinamen (Unterstrich vor Sprache, wie in bestehenden Dateien)
    file_de = kb_dir / f"{prefix}_{base_name}_de.md"
    file_en = kb_dir / f"{prefix}_{base_name}_en.md"
    
    # Speichern
    file_de.write_text(text_de, encoding='utf-8')
    file_en.write_text(text_en, encoding='utf-8')
    
    print(f"✅ Gespeichert:")
    print(f"   - {file_de}")
    print(f"   - {file_en}")

def main():
    if len(sys.argv) < 2:
        print("❌ Usage: python3 add_text_to_kb.py <input.txt> [--prefix 0001] [--title 'Custom Title']")
        sys.exit(1)
    
    input_file = Path(sys.argv[1])
    
    # Optionale Parameter
    prefix = "0001"
    custom_title = None
    
    for i, arg in enumerate(sys.argv):
        if arg == "--prefix" and i + 1 < len(sys.argv):
            prefix = sys.argv[i + 1]
        if arg == "--title" and i + 1 < len(sys.argv):
            custom_title = sys.argv[i + 1]
    
    if not input_file.exists():
        print(f"❌ Datei nicht gefunden: {input_file}")
        sys.exit(1)
    
    # Dateiname als Base
    base_name = input_file.stem.lower().replace(' ', '_')
    title = custom_title or input_file.stem.replace('_', ' ').title()
    
    print(f"📄 Verarbeite: {input_file.name}")
    print(f"📌 Prefix: {prefix}")
    print(f"📝 Titel: {title}")
    
    # Text einlesen
    text = input_file.read_text(encoding='utf-8')
    
    # Sprache erkennen
    source_lang = detect_language(text)
    print(f"🌐 Erkannte Sprache: {source_lang.upper()}")
    
    # Gemini konfigurieren
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ GEMINI_API_KEY nicht in .env gefunden!")
        sys.exit(1)
    
    client = genai.Client(api_key=api_key)
    model_name = 'gemini-2.0-flash-exp'
    
    print("🔄 Konvertiere zu Markdown...")
    markdown_source = convert_to_markdown(text, title)
    
    # Übersetzen
    if source_lang == 'de':
        print("🇩🇪 Deutsch erkannt → Übersetze nach Englisch...")
        text_de = markdown_source
        text_en = translate_to_english(text_de, client, model_name)
    else:
        print("🇬🇧 Englisch erkannt → Übersetze nach Deutsch...")
        text_en = markdown_source
        text_de = translate_to_german(text_en, client, model_name)
    
    # Speichern
    print("💾 Speichere in knowledge_base_final/...")
    save_to_knowledge_base(text_de, text_en, prefix, base_name)
    
    print("\n✅ FERTIG! Knowledge Base aktualisiert.")
    print("\n📋 Nächste Schritte:")
    print(f"   1. Review: cat knowledge_base_final/{prefix}_{base_name}.*.md")
    print(f"   2. Test: ./start_flask.sh")
    print(f"   3. Deploy: git add . && git commit -m 'KB: {title}' && git push")

if __name__ == "__main__":
    main()
