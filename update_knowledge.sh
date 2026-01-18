#!/bin/bash
###############################################################################
# update_knowledge.sh - Automatisiertes Knowledge Base Update Script
# 
# Verwendung:
#   ./update_knowledge.sh <dokument.pdf|dokument.docx|dokument.jpg>
#
# Dieses Script:
#   1. Aktiviert automatisch die richtige Virtual Environment (.venv_pipeline)
#   2. Verarbeitet das Dokument mit Marker-PDF + OpenAI Vision API
#   3. Übersetzt mit GPT-5.2 nach Deutsch und Englisch
#   4. Integriert in knowledge_base_final/
#   5. Zeigt Status-Updates während der Verarbeitung
###############################################################################

set -e  # Beende bei Fehler

# Farben für Terminal-Output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Projektverzeichnis
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

echo ""
echo "========================================================================"
echo -e "${GREEN}🚀 Knowledge Base Update - Automatische Dokumentenverarbeitung${NC}"
echo "========================================================================"
echo ""

# Prüfe, ob Dokument angegeben wurde
if [ -z "$1" ]; then
    echo -e "${RED}❌ Fehler: Kein Dokument angegeben!${NC}"
    echo ""
    echo "Verwendung:"
    echo "  ./update_knowledge.sh <pfad/zu/dokument.pdf>"
    echo ""
    echo "Beispiel:"
    echo "  ./update_knowledge.sh inputs/neues_zertifikat.pdf"
    echo ""
    exit 1
fi

INPUT_FILE="$1"

# Prüfe, ob Datei existiert
if [ ! -f "$INPUT_FILE" ]; then
    echo -e "${RED}❌ Fehler: Datei nicht gefunden: $INPUT_FILE${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Dokument gefunden:${NC} $INPUT_FILE"
echo ""

# Prüfe, ob .venv_pipeline existiert
if [ ! -d ".venv_pipeline" ]; then
    echo -e "${YELLOW}⚠️  .venv_pipeline nicht gefunden. Erstelle neue Virtual Environment...${NC}"
    python3 -m venv .venv_pipeline
    source .venv_pipeline/bin/activate
    pip install --upgrade pip
    pip install -r requirements_pipeline.txt
    echo -e "${GREEN}✅ Pipeline Environment erstellt!${NC}"
else
    echo -e "${GREEN}✅ Aktiviere Pipeline Environment (.venv_pipeline)${NC}"
    source .venv_pipeline/bin/activate
fi

echo ""
echo "========================================================================"
echo -e "${YELLOW}⏳ Starte Verarbeitung... (Dies kann einige Minuten dauern)${NC}"
echo "========================================================================"
echo ""

# Führe das Python-Script aus
python3 process_new_document.py

echo ""
echo "========================================================================"
echo -e "${GREEN}✨ Fertig! Dein Chatbot hat jetzt Zugriff auf das neue Wissen!${NC}"
echo "========================================================================"
echo ""
echo "📌 Nächste Schritte:"
echo "  1. Flask testen: Stelle eine Frage zum neuen Dokument"
echo "  2. Git-Deployment: git add . && git commit -m 'Update Knowledge Base' && git push"
echo ""
