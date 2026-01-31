# Rollback-Strategie: Systems Engineering ISO 15288 Knowledge Base

**Deployment:** 28. Januar 2026  
**Change:** Neue Knowledge Base für Systems Engineering nach ISO 15288

---

## ✅ Was wurde hinzugefügt?

**Neue Dateien:**
1. `knowledge_base_final/2026_01_systems_engineering_iso15288_de.md` (Deutsch)
2. `knowledge_base_final/2026_01_systems_engineering_iso15288_en.md` (Englisch)

**Inhalte:**
- **Value Engine** Architektur-Prinzipien
- ISO 15288 Standards-Integration
- **Impact Yield** mit 7:1 ROI-Metriken
- 20/80-Regel der Kostenfestschreibung
- Kernkonzepte:
  - **Emergence** (Torus Effect)
  - **Contextual Intelligence** & Systemgrenzen
  - **Execution Integrity** (Validierte Präzision)
- **Portfolio Health Hub**
- **Resonance Providers**
- 85% Kohärenz-Rate für strategische Agilität

---

## 🔄 Rollback-Optionen

### Option A: Schneller Rollback

```bash
# Zurück zum Stand vor SE-KB
git push origin v2026.01.28-before-se-kb:main --force
```

⚠️ **Warnung:** Force-Push überschreibt den aktuellen Stand!

---

### Option B: Sauberer Rollback (nur KB-Dateien entfernen)

```bash
# Nur die neuen KB-Dateien entfernen
git rm knowledge_base_final/2026_01_systems_engineering_iso15288_de.md
git rm knowledge_base_final/2026_01_systems_engineering_iso15288_en.md
git commit -m "revert: Remove Systems Engineering KB files"
git push origin main
```

---

## 🧪 Test-Checklist

**Lokal (nach Flask-Neustart):**
- [ ] Flask Server neu gestartet
- [ ] Deutsche Frage: "Was ist die Value Engine?"
- [ ] Deutsche Frage: "Erkläre ISO 15288"
- [ ] Englische Frage: "What is the Torus Effect?"
- [ ] Englische Frage: "Explain Impact Yield"
- [ ] Antworten enthalten SE-Konzepte (Emergence, Contextual Intelligence, etc.)

**Live (auf Render nach Deploy):**
- [ ] Chatbot öffnet sich ohne Fehler
- [ ] SE-Fragen funktionieren in beiden Sprachen
- [ ] Keine 500-Fehler im Render-Log
- [ ] Antwortzeit < 5 Sekunden

---

## 📊 Git-Historie

- `21b40f7`: fix: Prevent contact page from disappearing on hover
- `9d2217f`: feat: Add Systems Engineering ISO 15288 knowledge base (← AKTUELL)

---

## 🆘 Notfall-Handling

**Falls Chatbot SE-Inhalte nicht kennt:**
1. Prüfe: Sind die Dateien in `knowledge_base_final/` vorhanden?
2. Flask Server neu starten (lädt KB neu)
3. Teste lokal vor Live-Test

**Falls Render-Deploy fehlschlägt:**
1. Render Dashboard öffnen
2. Build-Log prüfen
3. "Manual Deploy" mit "Clear build cache"

---

**Erstellt:** 28. Jan 2026  
**Autor:** AI Assistant
