# Rollback-Strategie: Language Detection Fix

**Deployment:** 26. Januar 2025  
**Change:** Verbesserte deutsche Spracherkennung im Chatbot

---

## ✅ Was wurde geändert?

1. **Erweiterte deutsche Keywords** in `app.py`:
   - Hinzugefügt: `kennt`, `kenne`, `kennen`, `gibt`, `gib`, `nenne`, `nennt`, `macht`, `mach`, `arbeitet`, `arbeit`
   
2. **Verstärkte System-Prompts**:
   - Explizitere Sprachanweisungen für Gemini mit Emoji-Warnings (🇩🇪/🇬🇧)
   - Härtere Formulierung: "Wenn du auch nur ein einziges englisches Wort verwendest, ist die Antwort falsch"

3. **Debug-Logging**:
   - `print(f"🔍 LANGUAGE DETECTION: '{user_message[:50]}...' → {detected_lang}")`

---

## 🔄 Rollback-Optionen

### Option A: Zurück zur vorherigen Version (schnell)

```bash
# Lokal testen:
git checkout v2025.01.26-before-language-fix
flask run

# Wenn OK, dann live deployen:
git push origin v2025.01.26-before-language-fix:main --force
```

**Warnung:** Force-Push überschreibt den aktuellen Stand!

---

### Option B: Einzelne Änderungen rückgängig machen (sauber)

```bash
# Nur die app.py zurücksetzen
git checkout v2025.01.26-before-language-fix -- app.py
git add app.py
git commit -m "revert: Rollback language detection changes"
git push origin main
```

---

## 🧪 Test-Checklist nach Deployment

**Lokal (vor Render):**
- [ ] Flask Server läuft ohne Fehler
- [ ] Deutsche Frage: "kennt karsten soziale systeme" → Antwort auf Deutsch
- [ ] Englische Frage: "does karsten know social systems" → Antwort auf Englisch
- [ ] Terminal-Log zeigt: `🔍 LANGUAGE DETECTION: 'kennt karsten...' → de`

**Live (auf Render):**
- [ ] Chatbot öffnet sich
- [ ] Selbe Tests wie oben
- [ ] Keine 500-Fehler im Render-Log
- [ ] Antwortzeit < 5 Sekunden

---

## 📊 Git-Historie

- `f482b63`: feat: Add Complexity Primer KB + CTA buttons
- `006783d`: fix: Improve German language detection (← AKTUELL)

---

## 🆘 Notfall-Kontakt

Falls Render nicht automatisch deployt oder Fehler auftreten:

1. Render-Dashboard öffnen: https://dashboard.render.com
2. Service: `karport2025` auswählen
3. "Manual Deploy" → "Clear build cache & deploy"
4. Logs prüfen auf Python-Fehler

---

**Erstellt:** 26. Jan 2025  
**Autor:** AI Assistant
