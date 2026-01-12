import os
from openai import OpenAI
from pathlib import Path

# API Key direkt setzen
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    # Versuche aus .env zu laden
    env_file = Path(".env")
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            if line.startswith("OPENAI_API_KEY="):
                api_key = line.split("=", 1)[1].strip()
                break

client = OpenAI(api_key=api_key)

# Lade deutsche Version
with open("knowledge_base_final/0000_Methodische_Landkarte_de.md", "r", encoding="utf-8") as f:
    de_content = f.read()

print("Übersetze ins Englische mit GPT-5.2...")

prompt = f"""
Du bist ein Experte für Projektmanagement-Zertifizierungen, Geschäftsprozessmanagement, Complex adaptive systems, Konstruktivismus und Systemtheorie, Ökonomie, Betriebswirtschaft, General Semantics, Zen-Buddhismus, Taoismus und Karriere-Consulting.
Übersetze den folgenden Markdown-Inhalt für die Webseite 'zenk-pm-now.de' ins Englisch.

ANWEISUNGEN:
1. Behalte die Markdown-Struktur (Tabellen, Fettdruck, Header) exakt bei.
2. Nutze korrekte Fachterminologie (z.B. Systems Theory, Constructivism, Cybernetics).
3. Namen von Vordenkern NICHT übersetzen (Niklas Luhmann bleibt Niklas Luhmann).
4. Der Ton soll professionell und akademisch sein.
5. Gib nur den übersetzten Text zurück.

TEXT:
{de_content}
"""

response = client.chat.completions.create(
    model="gpt-5.2",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.3
)

en_content = response.choices[0].message.content

# Speichere englische Version
with open("knowledge_base_final/0000_Methodische_Landkarte_en.md", "w", encoding="utf-8") as f:
    f.write(en_content)

print("✓ Englische Version erstellt!")
print(f"✓ {len(en_content)} Zeichen")


