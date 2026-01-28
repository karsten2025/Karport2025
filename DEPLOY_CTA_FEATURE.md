# Deploy: CTA Feature + Complexity Primer KB

**Datum:** 2026-01-26  
**Commit:** `f482b63` - feat: Add Complexity Primer KB + CTA buttons for lead generation

---

## Was wurde geändert?

### 1. Chatbot CTA-Button
- **Datei:** `static/js/main.js`, `static/css/style.css`
- **Feature:** Nach jeder Bot-Antwort erscheint "💼 Projekt besprechen" Button
- **Funktion:** Schließt Chat, scrollt zur Kontakt-Section

### 2. Direkte E-Mail auf Kontaktseite
- **Dateien:** `templates/partials/profile-contact.de.html`, `profile-contact.en.html`
- **Feature:** Direkter mailto-Link zu `karsten.zenk@gmail.com`
- **Sicherheit:** Funktioniert auch wenn Formspree ausfällt

### 3. Knowledge Base erweitert
- 12 neue Complexity-Dateien (copyright-safe, paraphrasiert)
- Alle internen KB-Verweise aus Prompts entfernt
- Test-Script (`kb_test.py`) für automatisierte Qualitätsprüfung

---

## Deploy-Schritte (manuell)

```bash
# 1. Sicherheits-Tag erstellen (für Rollback)
git tag -a pre-cta-deploy-$(date +%Y%m%d) -m "Before CTA feature"

# 2. Push (inkl. Tags)
git push origin main
git push --tags
```

**Render deployt automatisch nach dem Push.**

---

## Rollback-Strategie (falls etwas schiefgeht)

### Option A: Schnelles Rollback (über Render Dashboard)
1. Gehe zu **Render.com → Dashboard → dein Service**
2. Klicke auf "Manual Deploy" → Wähle den vorherigen Commit `be0a213`
3. Render baut sofort die alte Version

### Option B: Git-Rollback (lokal)
```bash
# Zurück zum letzten funktionierenden Stand
git reset --hard be0a213

# Force-Push (ACHTUNG: überschreibt Remote)
git push origin main --force

# Render deployt automatisch die alte Version
```

### Option C: Nur CTA rückgängig machen (Hotfix)
Falls nur der CTA-Button Probleme macht:

```bash
# In static/js/main.js die Zeile entfernen:
# addCTA();

# In static/css/style.css die Klassen entfernen:
# .kz-cta-container, .kz-cta-btn

# Commit + Push
git add static/js/main.js static/css/style.css
git commit -m "hotfix: remove CTA button temporarily"
git push origin main
```

---

## Test-Checklist (nach Deploy)

- [ ] Chatbot öffnen, Frage stellen → CTA-Button erscheint?
- [ ] CTA-Button klicken → Kontakt-Section öffnet?
- [ ] Direkter E-Mail-Link funktioniert?
- [ ] Keine "Complexity Primer" oder "knowledge base" Verweise in Antworten?
- [ ] Desktop + Mobile testen

---

## Aktueller Commit-Hash

**Letzte funktionierende Version (Hologram):** `be0a213`  
**Neue Version (CTA Feature):** `f482b63`

Bei Problemen: `git reset --hard be0a213 && git push --force origin main`
