# 🎯 Alias Cheat Sheet - Knowledge Base Management

## ⚡ Super-Befehle (von überall nutzbar)

### `kbdeploy` - Komplettes Deployment 🚀
```bash
kbdeploy inputs/dokument.pdf
```
**Macht:**
- ✅ Dokument verarbeiten (Marker + GPT-5.2)
- ✅ Optional: Lokaler Flask-Test
- ✅ Git commit + push
- ✅ Render Dashboard öffnen

**Empfohlen für:** Normale Updates

---

### `kbupdate` - Nur Verarbeitung ⚡
```bash
kbupdate inputs/dokument.pdf
```
**Macht:**
- ✅ Dokument verarbeiten (Marker + GPT-5.2)
- ❌ KEIN Git (machst du manuell)

**Empfohlen für:** Wenn du mehrere Dokumente batch-verarbeiten willst

---

### `flaskstart` - Flask starten 🌐
```bash
flaskstart
```
**Macht:**
- ✅ Port 5001 freigeben
- ✅ Flask auf Port 5001 starten

**Empfohlen für:** Lokale Tests

---

### `cdkb` - Ins Projekt 📁
```bash
cdkb
```
**Macht:**
- ✅ Wechselt ins Projekt-Verzeichnis

**Empfohlen für:** Schneller Projekt-Zugriff

---

### `killport` - Port freigeben 🔪
```bash
killport 5001
```
**Macht:**
- ✅ Stoppt alle Prozesse auf dem Port

**Empfohlen für:** Port-Konflikte lösen

---

## 🎯 Workflow-Beispiele

### Beispiel 1: Schnelles Update (5 Min)
```bash
# 1. Dokument kopieren
cp ~/Downloads/2026_02_Certificate.pdf inputs/

# 2. Komplett deployen
kbdeploy inputs/2026_02_Certificate.pdf

# 3. Auf "Lokaler Test?" mit 'n' antworten

# 4. Fertig! Render deployed automatisch
```

### Beispiel 2: Mit lokalem Test (7 Min)
```bash
# 1. Dokument kopieren
cp ~/Downloads/new_doc.pdf inputs/

# 2. Deployen
kbdeploy inputs/new_doc.pdf

# 3. Auf "Lokaler Test?" mit 'j' antworten

# 4. Im Browser testen

# 5. STRG+C wenn fertig

# 6. Render deployed automatisch
```

### Beispiel 3: Batch-Verarbeitung (10 Min)
```bash
# Mehrere Dokumente:
kbupdate inputs/doc1.pdf
kbupdate inputs/doc2.pdf
kbupdate inputs/doc3.pdf

# Dann einmal Git:
git add knowledge_base_final/
git commit -m "Add: 3 neue Dokumente"
git push origin main
```

### Beispiel 4: Nur lokal testen
```bash
# Flask starten
flaskstart

# Im Browser: http://localhost:5001
# Testen...

# STRG+C zum Beenden
```

---

## 🆘 Troubleshooting

### Problem: "command not found: kbdeploy"
```bash
# Lösung: .zshrc neu laden
source ~/.zshrc
```

### Problem: Port 5001 belegt
```bash
# Lösung: Port freigeben
killport 5001
```

### Problem: Script-Fehler
```bash
# Lösung: Ins Projekt wechseln und manuell prüfen
cdkb
./kb-deploy.sh inputs/dokument.pdf
```

---

## 📝 Alias-Liste (Referenz)

| Alias | Funktion | Verwendung |
|-------|----------|------------|
| `kbdeploy` | Komplettes Deployment | `kbdeploy inputs/dok.pdf` |
| `kbupdate` | Nur Verarbeitung | `kbupdate inputs/dok.pdf` |
| `flaskstart` | Flask starten | `flaskstart` |
| `cdkb` | Ins Projekt | `cdkb` |
| `killport` | Port freigeben | `killport 5001` |

---

## 🎓 Pro-Tips

1. **Tab-Completion funktioniert:**
   ```bash
   kbdeploy inputs/<TAB>
   # Zeigt alle Dateien in inputs/
   ```

2. **Aliases zeigen:**
   ```bash
   type kbdeploy
   # Zeigt was der Alias macht
   ```

3. **Historie durchsuchen:**
   ```bash
   history | grep kbdeploy
   # Zeigt alle kbdeploy-Aufrufe
   ```

4. **Ein-Zeiler für alles:**
   ```bash
   cp ~/Downloads/cert.pdf inputs/ && kbdeploy inputs/cert.pdf
   ```

---

**Erstellt:** 2026-01-18  
**Version:** 1.0  
**Für:** Karsten Zenk - Portfolio Project
