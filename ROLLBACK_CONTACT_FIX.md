# Rollback-Strategie: Contact Page Hover Fix

**Deployment:** 28. Januar 2026  
**Change:** Kontaktseite verschwindet nicht mehr beim Hovern über Navigation

---

## ✅ Was wurde geändert?

**Problem:** Wenn man auf "Projekt besprechen" klickt und die Kontaktseite lädt, verschwindet diese beim Hovern über die rechte Navigation (Zertifikate).

**Lösung:** `static/js/main.js` erweitert mit Content-Lock-Mechanismus:

1. **contentIsLocked Flag:** Merkt sich, wenn eine "echte" Seite (Kontakt, Über mich, etc.) geladen wurde
2. **Geschütztes Mouseout:** Setzt Inhalt nur zurück, wenn keine gelockte Seite aktiv ist
3. **Smart Unlock:** Beim Hover über Zertifikate wird temporär entsperrt für Previews

---

## 🔄 Rollback-Optionen

### Option A: Schneller Rollback (bei kritischem Fehler)

```bash
git push origin v2026.01.28-before-contact-fix:main --force
```

⚠️ **Warnung:** Force-Push überschreibt den aktuellen Stand!

---

### Option B: Sauberer Rollback (empfohlen)

```bash
git checkout v2026.01.28-before-contact-fix -- static/js/main.js
git add static/js/main.js
git commit -m "revert: Rollback contact page hover fix"
git push origin main
```

---

## 🧪 Test-Checklist

**Lokal (vor Live):**
- [ ] Chatbot öffnet sich
- [ ] "Projekt besprechen" klicken → Kontaktseite lädt
- [ ] Mit Maus über rechte Navigation (Zertifikate) hovern
- [ ] Maus wieder raus → Kontaktseite bleibt sichtbar ✅
- [ ] Zertifikat hovern → Preview funktioniert ✅

**Live (nach Render-Deploy):**
- [ ] Selbe Tests wie oben
- [ ] Keine JavaScript-Fehler in Browser-Console
- [ ] Navigation funktioniert flüssig

---

## 📊 Git-Historie

- `006783d`: fix: Improve German language detection
- `21b40f7`: fix: Prevent contact page from disappearing on hover (← AKTUELL)

---

## 🆘 Notfall-Kontakt

Falls JavaScript-Fehler auftreten:

1. Browser-Console öffnen (F12)
2. Fehler kopieren
3. Schneller Rollback mit Option A
4. Fehler analysieren

---

**Erstellt:** 28. Jan 2026  
**Autor:** AI Assistant
