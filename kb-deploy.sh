#!/bin/bash
###############################################################################
# kb-deploy.sh - Complete Knowledge Base Update & Deployment
# 
# Usage: ./kb-deploy.sh <dokument.pdf>
#
# This script automates the COMPLETE workflow:
# 1. Process document (Marker + GPT-5.2)
# 2. Local Flask test
# 3. Git commit & push
# 4. Opens Render dashboard
###############################################################################

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

# Project directory
PROJECT_DIR="/Users/karsten/Documents/Webinars/Webdev-Fulls-Stack/Portfolio - Karsten-Zenk-10012025-Cursor"
cd "$PROJECT_DIR"

echo ""
echo "========================================================================"
echo -e "${GREEN}🚀 Complete Knowledge Base Update & Deployment${NC}"
echo "========================================================================"
echo ""

# Check if document is provided
if [ -z "$1" ]; then
    echo -e "${RED}❌ Fehler: Kein Dokument angegeben!${NC}"
    echo ""
    echo "Verwendung:"
    echo "  ./kb-deploy.sh <pfad/zu/dokument.pdf>"
    echo ""
    echo "Beispiel:"
    echo "  ./kb-deploy.sh inputs/2026_02_Certificate.pdf"
    echo ""
    exit 1
fi

INPUT_FILE="$1"
BASENAME=$(basename "$INPUT_FILE" | sed 's/\.[^.]*$//')

# Check if file exists
if [ ! -f "$INPUT_FILE" ]; then
    echo -e "${RED}❌ Fehler: Datei nicht gefunden: $INPUT_FILE${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Dokument gefunden:${NC} $INPUT_FILE"
echo ""

# Step 1: Process document
echo "========================================================================"
echo -e "${YELLOW}📄 SCHRITT 1: Dokument verarbeiten${NC}"
echo "========================================================================"
./update_knowledge.sh "$INPUT_FILE"

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Fehler bei der Verarbeitung!${NC}"
    exit 1
fi

# Step 2: Local test (optional)
echo ""
echo "========================================================================"
echo -e "${YELLOW}🧪 SCHRITT 2: Lokaler Test (OPTIONAL)${NC}"
echo "========================================================================"
echo ""
read -p "Möchtest du lokal testen? (j/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Jj]$ ]]; then
    echo -e "${BLUE}Starte Flask auf http://localhost:5001${NC}"
    echo "Drücke STRG+C wenn fertig mit Testen..."
    echo ""
    
    killport 5001 2>/dev/null || true
    sleep 1
    
    source .venv/bin/activate
    python3 -m flask run --port 5001
    
    echo ""
    echo -e "${GREEN}✅ Test abgeschlossen${NC}"
fi

# Step 3: Git commit & push
echo ""
echo "========================================================================"
echo -e "${YELLOW}📦 SCHRITT 3: Git Deployment${NC}"
echo "========================================================================"
echo ""

# Show changes
git status

# Add files
echo ""
echo -e "${BLUE}Füge neue Dateien hinzu...${NC}"
git add "knowledge_base_final/${BASENAME}_de.md" "knowledge_base_final/${BASENAME}_en.md"

# Commit
COMMIT_MSG="Add: ${BASENAME} zur Knowledge Base"
echo -e "${BLUE}Commit: ${COMMIT_MSG}${NC}"
git commit -m "$COMMIT_MSG"

# Push
echo -e "${BLUE}Push zu GitHub...${NC}"
git push origin main

echo ""
echo -e "${GREEN}✅ Git Deployment erfolgreich!${NC}"

# Step 4: Open Render dashboard
echo ""
echo "========================================================================"
echo -e "${YELLOW}🌐 SCHRITT 4: Render Deployment${NC}"
echo "========================================================================"
echo ""
echo -e "${BLUE}Öffne Render Dashboard...${NC}"
open "https://dashboard.render.com" 2>/dev/null || echo "Öffne manuell: https://dashboard.render.com"

echo ""
echo "========================================================================"
echo -e "${GREEN}✨ DEPLOYMENT ABGESCHLOSSEN!${NC}"
echo "========================================================================"
echo ""
echo "📌 Nächste Schritte:"
echo "  1. Prüfe Render Dashboard für Deploy-Status"
echo "  2. Warte ~3-4 Minuten"
echo "  3. Teste auf zenk-pm-now.de"
echo ""
echo -e "${GREEN}🎉 Neues Wissen ist bald live!${NC}"
echo ""
