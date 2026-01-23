# 📋 Knowledge Base Update - Quick Reference

## 🚀 Der 5-Minuten-Workflow

### **Schritt 1: Dokument ablegen** (10 Sek)
```bash
cp ~/Downloads/NEUES_DOKUMENT.pdf \
   "/Users/karsten/Documents/Webinars/Webdev-Fulls-Stack/Portfolio - Karsten-Zenk-10012025-Cursor/inputs/"
```

### **Schritt 2: Automatische Verarbeitung** (30-60 Sek)
```bash
cd "/Users/karsten/Documents/Webinars/Webdev-Fulls-Stack/Portfolio - Karsten-Zenk-10012025-Cursor"
./update_knowledge.sh inputs/NEUES_DOKUMENT.pdf
```

**Was passiert automatisch:**
- ✅ Marker-PDF: Dokument → Markdown
- ✅ GPT-5.2: Übersetzung (DE + EN)
- ✅ Speichern in `knowledge_base_final/`

### **Schritt 3: Lokaler Test (OPTIONAL)** (2 Min)
```bash
killport 5001
./start_flask.sh
# Browser: http://localhost:5001
# Testfrage stellen!
```

### **Schritt 4: Git Deployment** (30 Sek)
```bash
git add knowledge_base_final/*NEUES_DOKUMENT*
git commit -m "Add: NEUES_DOKUMENT zur Knowledge Base"
git push origin main
```

### **Schritt 5: Warten auf Render** (3-4 Min)
- ✅ Automatischer Deploy
- ✅ Live auf zenk-pm-now.de

---

## 🆘 Troubleshooting

### **Problem: Port 5001 belegt**
```bash
killport 5001
```

### **Problem: Flask nicht gefunden**
```bash
python3 -m flask run --port 5001
```

### **Problem: Script-Fehler**
```bash
# Prüfe .venv_pipeline
source .venv_pipeline/bin/activate
pip install -r requirements_pipeline.txt
```

### **Problem: Marker dauert zu lange**
```bash
# Normal für große PDFs (1-2 Min pro 10 Seiten)
# Einfach Kaffee holen ☕
```

---

## 📦 Supported Formate

- ✅ **PDF** - Alle Arten
- ✅ **DOCX** - Word-Dokumente
- ✅ **JPG/PNG** - Mit OCR
- ✅ **Multi-Page** - Beliebig groß

---

## 🎯 Best Practices

1. **Dateinamen:** Nutze sprechende Namen
   - ✅ `2026_02_AI_Certificate.pdf`
   - ❌ `download (3).pdf`

2. **Ein Dokument nach dem anderen**
   - Besser als Batch-Processing
   - Einfacher zu testen

3. **Lokal testen vor Deploy**
   - Verhindert Fehler live
   - 2 Minuten gut investiert

4. **Git-Messages klar formulieren**
   - ✅ `"Add: 2026_02_AI_Certificate"`
   - ❌ `"update"`

---

## ⚡ Power-User Shortcuts

### **One-Liner (Copy & Paste)**
```bash
cd "/Users/karsten/Documents/Webinars/Webdev-Fulls-Stack/Portfolio - Karsten-Zenk-10012025-Cursor" && \
./update_knowledge.sh inputs/DOKUMENT.pdf && \
git add knowledge_base_final/*DOKUMENT* && \
git commit -m "Add: DOKUMENT" && \
git push origin main
```

### **Alias in .zshrc hinzufügen**
```bash
# Füge zu ~/.zshrc hinzu:
alias kb-update='cd "/Users/karsten/Documents/Webinars/Webdev-Fulls-Stack/Portfolio - Karsten-Zenk-10012025-Cursor" && ./update_knowledge.sh'

# Dann einfach:
kb-update inputs/neues_dokument.pdf
```

---

## 📞 Support

Bei Problemen:
1. Prüfe Git-Status: `git status`
2. Prüfe Flask-Logs: Terminal-Output
3. Prüfe Render-Dashboard: https://dashboard.render.com

---

**Erstellt:** 2026-01-18  
**Version:** 1.0  
**Projekt:** Portfolio Karsten Zenk
