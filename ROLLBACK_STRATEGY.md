# 🛡️ Rollback-Strategie für Hologram-Deploy

## Aktueller Stand
- **Commit vor Deploy:** `4d5b056` (perf(etappe3): JS cleanup, Flask-Compress)
- **Neuer Commit:** `be0a213` (feat(hologram): Re-implement Header Hologram)
- **Git Tag:** `pre-hologram-deploy-YYYYMMDD-HHMM` (als Backup erstellt)

## ⚠️ Falls der Deploy auf Render Probleme verursacht:

### Option 1: Schneller Rollback (Empfohlen)
```bash
# Zurück zum Commit vor Hologram
git reset --hard 4d5b056
git push origin main --force
```

### Option 2: Hologram-Komponente deaktivieren (sanfter)
```bash
# Nur die Hologram-Integration entfernen, Rest behalten
# In templates/index.html: Header-Hologram-Include auskommentieren
# In templates/index.html: header_hologram.js Script-Tag entfernen
```

### Option 3: Vollständiger Rollback mit Tag
```bash
# Zum Tag zurückkehren (falls vorhanden)
git reset --hard pre-hologram-deploy-YYYYMMDD-HHMM
git push origin main --force
```

## 📋 Checkliste nach Rollback:
1. ✅ Render-Deploy abwarten (automatisch nach Push)
2. ✅ Desktop testen (zenk-pm-now.de)
3. ✅ Mobile testen (iPhone/Android)
4. ✅ Chatbot-Funktionalität prüfen
5. ✅ Torus-Launcher prüfen

## 🔍 Debugging bei Problemen:
```bash
# Render-Logs prüfen
# Im Render-Dashboard: Logs-Tab öffnen

# Lokal testen
./start_flask.sh
# Dann: http://localhost:5001
```

---
**Erstellt:** $(date)
**Commit:** be0a213
