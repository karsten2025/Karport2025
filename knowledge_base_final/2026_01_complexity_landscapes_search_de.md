---
Title: "Komplexitäts‑Primer — Landschaften & Suche"
Quelle: Paraphrase (Scott E. Page)
Sprache: de
Tags: landschaft, suche, optimisation
Lizenzhinweis: Transformative Paraphrase für interne Knowledge Base Nutzung
---

# Landschafts‑Metapher & Suche

Landschaften‑Metapher
- Die sogenannte "Fitness‑Landschaft" visualisiert Lösungsqualität: Mount‑Fuji (ein Gipfel), Rugged (viele lokale Gipfel), Dancing (Gipfel verschieben sich, da Akteure adaptieren).

Implikationen für Design und Suche
- Mount‑Fuji: Greedy-/Gradientensuche funktioniert gut.
- Rugged: Explorationsstrategien nötig (z. B. simulated annealing, randomisierte Suche).
- Dancing: Kontinuierliche Exploration; Optimierungsziele verschieben sich mit der Zeit.

Praktische Regeln
1. Vor Auswahl einer Suchstrategie zuerst Landschaftstyp diagnostizieren.  
2. Stufenweise Exploration: zu Beginn mehr Zufall, später gezielte Ausbeutung.  
3. Favorisiere Experimente und gestaffelte Rollouts statt einmaliger Optimierung auf dynamischen Landschaften.
