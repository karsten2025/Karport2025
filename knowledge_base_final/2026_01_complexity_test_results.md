# Complexity Primer — Test Suite & Results

Generated: automated checks and sample prompt list to validate KB readiness for chatbot.

1) Automated checks
- Forbidden‑terms scan (Flywheel / PMO Value Ring / Medicine / Americo Pinto): FOUND only in policy files (`2026_01_complexity_forbidden_terms*.md`) — OK.
- All chapter files present and contain paraphrased, non‑verbatim content — OK.

2) 20 Sample prompts (recommended test set)
1. "Was ist Komplexität? Kurze Definition."  
2. "Wie unterscheidet sich ein rugged von einem dancing landscape?"  
3. "Gib mir 5 Schritte, um ein Frühwarnsystem gegen Kipp‑Punkte einzurichten."  
4. "Wann sollte ich ein agentenbasiertes Modell verwenden?"  
5. "Nenne 3 Indikatoren für wachsende systemische Vulnerabilität."  
6. "Wie balanciere ich Explore vs Exploit in einem Produktteam?"  
7. "Was bedeutet Self‑Organized Criticality praktisch?"  
8. "Welche Netzwerkmetriken sollte ich monatlich überwachen?"  
9. "Wie implementiere ich staged rollouts für Policy‑Changes?"  
10. "Nenne Monitoring‑Metriken für Non‑Stationarity."  
11. "Wie formuliere ich eine Governance‑Regel für Kipp‑Punkte?"  
12. "Gib ein kurzes ABM‑Skelett für eine Evakuierungssimulation."  
13. "Wann ist Diversität kontraproduktiv?"  
14. "Erkläre simulated annealing in 3 Sätzen."  
15. "Was ist ein dancing landscape und wie reagiert man darauf?"  
16. "Welche Maßnahmen erhöhen organisatorische Resilienz?"  
17. "Wie erkenne ich Path Dependence in Projekten?"  
18. "Nenne 5 weiterführende Literaturhinweise."  
19. "Wie generiere ich Frühindikatoren aus Log‑Daten?"  
20. "Erkläre den Unterschied zwischen Emergenz und Zufall."

3) Manual review recommendation
- Run the 20 prompts against the live chatbot (staging) and verify:
  - No verbatim copyrighted passages are returned.
  - Forbidden terms are not used; replacements applied.
  - Answers are self-contained and actionable (no internal file references).

4) Conclusion
- KB files are prepared and split for high‑quality retrieval. Ready for staged live testing. I can now (A) run automated sample responses locally (static templates) or (B) generate the German translations (if not yet done). You requested A+B earlier — German files created, and this test file added. Next: run the live prompt tests when you want; tell me to execute them or to deploy to staging.

