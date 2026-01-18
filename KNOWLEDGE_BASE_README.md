# 📚 Knowledge Base Management - Dokumentation

## 🎯 Übersicht

Dieses Projekt nutzt eine **2-VEnv-Architektur** für optimale Trennung von Flask-Deployment und Dokument-Verarbeitung.

---

## 📁 Virtual Environments

### `.venv` - Flask Production (50 MB)
**Verwendung:** Web-Deployment, Flask-Server

**Dependencies:**
- flask
- python-dotenv
- google-genai
- gunicorn
- langdetect

**Aktivieren:**
```bash
source .venv/bin/activate
flask run
```

---

### `.venv_pipeline` - Dokument-Verarbeitung (2 GB)
**Verwendung:** Knowledge Base Updates (Marker-PDF, GPT-5.2)

**Dependencies:**
- openai (GPT-5.2 Übersetzungen)
- marker-pdf (PDF/DOCX/Bild → Markdown)
- python-docx, weasyprint, mammoth
- psutil

**Aktivieren:**
```bash
source .venv_pipeline/bin/activate
python process_new_document.py
```

---

## 🚀 Quick Start

### Neues Dokument zur Knowledge Base hinzufügen

**Schritt 1:** Dokument ablegen
```bash
cp /pfad/zu/dokument.pdf inputs/
```

**Schritt 2:** Automatische Verarbeitung
```bash
./update_knowledge.sh inputs/dokument.pdf
```

Das Script führt automatisch aus:
1. ✅ Marker-PDF Konvertierung (PDF/DOCX → Markdown)
2. ✅ GPT-5.2 Übersetzung (Deutsch + Englisch)
3. ✅ Integration in `knowledge_base_final/`
4. ✅ Automatisch verfügbar für Flask-Chatbot!

---

### Flask starten

```bash
./start_flask.sh
```

Öffne: http://localhost:5001

---

## 🔧 Manuelle Nutzung

### Knowledge Base Update (manuell)

```bash
# Aktiviere Pipeline-VEnv
source .venv_pipeline/bin/activate

# Führe Verarbeitung aus
python3 process_new_document.py

# Deaktiviere
deactivate
```

### Flask starten (manuell)

```bash
# Aktiviere Flask-VEnv
source .venv/bin/activate

# Starte Server
flask run --port 5001

# Deaktiviere
deactivate
```

---

## 📂 Verzeichnisstruktur

```
Portfolio-Karsten-Zenk/
├── .venv/                          # Flask Production VEnv (50 MB)
│   └── requirements.txt
│
├── .venv_pipeline/                 # Pipeline VEnv (2 GB)
│   └── requirements_pipeline.txt
│
├── inputs/                         # Neue Dokumente hier ablegen
│   └── Lebenslauf_Karsten_Zenk.docx
│
├── inputs_out/                     # Temporäre Marker-Outputs
│
├── knowledge_base_final/           # Finale Knowledge Base (DE + EN)
│   ├── 0000_Methodische_Landkarte_de.md
│   ├── 0000_Methodische_Landkarte_en.md
│   ├── Lebenslauf_Karsten_Zenk_de.md
│   ├── Lebenslauf_Karsten_Zenk_en.md
│   └── ... (184 Dateien)
│
├── app.py                          # Flask Application
├── process_new_document.py         # Pipeline-Script
├── update_knowledge.sh             # Wrapper für Knowledge Updates
├── start_flask.sh                  # Wrapper für Flask
└── .flaskenv                       # Flask-Konfiguration (Port 5001)
```

---

## 🧪 Workflow-Beispiel

### 1. Neues Zertifikat hinzufügen

```bash
# Schritt 1: Dokument ablegen
cp ~/Downloads/2026_01_AI_Certificate.pdf inputs/

# Schritt 2: Verarbeiten
./update_knowledge.sh inputs/2026_01_AI_Certificate.pdf

# Output:
# ✅ Marker-PDF erfolgreich
# ✅ Übersetzung Deutsch → knowledge_base_final/2026_01_AI_Certificate_de.md
# ✅ Übersetzung Englisch → knowledge_base_final/2026_01_AI_Certificate_en.md
```

### 2. Flask neu starten (lädt automatisch neue KB)

```bash
./start_flask.sh
```

### 3. Testen

Frage im Chatbot (Deutsch):
> "Welche KI-Zertifikate hat Karsten 2026 erworben?"

Frage im Chatbot (Englisch):
> "What AI certifications did Karsten earn in 2026?"

→ Der Bot antwortet **automatisch in der Sprache der Frage**!

---

## 🔄 Git-Deployment

```bash
# Neue Knowledge Base committen
git add knowledge_base_final/
git add requirements_pipeline.txt
git commit -m "Add: 2026_01_AI_Certificate"
git push origin main
```

**Wichtig:** Nur `knowledge_base_final/` wird deployed, NICHT `.venv_pipeline`!

---

## 🛠️ Troubleshooting

### Problem: Port 5001 bereits belegt

```bash
# Automatisch gelöst durch start_flask.sh
# Oder manuell:
kill $(lsof -t -i:5001)
```

### Problem: Marker-PDF findet Datei nicht

```bash
# Prüfe, ob Dokument in inputs/ liegt
ls -la inputs/

# Prüfe Marker-Output
ls -la inputs_out/
```

### Problem: GPT-5.2 API-Fehler

```bash
# Prüfe .env
cat .env | grep OPENAI_API_KEY

# Teste API-Key
source .venv_pipeline/bin/activate
python check_models.py
```

---

## 📊 Performance

| Task | Dauer | VEnv |
|------|-------|------|
| Single PDF (10 Seiten) | ~30 Sek | `.venv_pipeline` |
| GPT-5.2 Translation | ~10 Sek/Sprache | `.venv_pipeline` |
| Flask Start | ~2 Sek | `.venv` |
| Knowledge Base Reload | Automatisch | `.venv` |

---

## 🎓 Supported Formate

- ✅ PDF
- ✅ DOCX
- ✅ JPG / PNG (OCR via Marker-PDF)
- ✅ Multi-Page Dokumente

---

## 📝 Wartung

### VEnv neu aufbauen (Flask)

```bash
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### VEnv neu aufbauen (Pipeline)

```bash
rm -rf .venv_pipeline
python3 -m venv .venv_pipeline
source .venv_pipeline/bin/activate
pip install -r requirements_pipeline.txt
```

---

## 🚀 Nächste Schritte

1. ✅ Dokument in `inputs/` ablegen
2. ✅ `./update_knowledge.sh inputs/dokument.pdf` ausführen
3. ✅ `./start_flask.sh` für Flask
4. ✅ Testen im Browser
5. ✅ Git-Deployment

**Viel Erfolg! 🎉**
