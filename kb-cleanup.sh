#!/bin/bash
###############################################################################
# kb-cleanup.sh - Remove documents from Knowledge Base
# 
# Usage: 
#   ./kb-cleanup.sh <dokument-name>
#   ./kb-cleanup.sh cert1.pdf
#
# This script removes:
# 1. Document from knowledge_base_final/ (DE + EN)
# 2. Optionally: Original from inputs/
# 3. Creates Git commit
###############################################################################

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

PROJECT_DIR="/Users/karsten/Documents/Webinars/Webdev-Fulls-Stack/Portfolio - Karsten-Zenk-10012025-Cursor"
cd "$PROJECT_DIR"

echo ""
echo "========================================================================"
echo -e "${RED}🗑️  Knowledge Base Cleanup${NC}"
echo "========================================================================"
echo ""

# Check if document name is provided
if [ -z "$1" ]; then
    echo -e "${RED}❌ Fehler: Kein Dokument angegeben!${NC}"
    echo ""
    echo "Verwendung:"
    echo "  ./kb-cleanup.sh <dokument-name>"
    echo ""
    echo "Beispiele:"
    echo "  ./kb-cleanup.sh cert1.pdf"
    echo "  ./kb-cleanup.sh 2025_02_Old_Certificate"
    echo ""
    echo "💡 Tipp: Du kannst mit oder ohne Dateiendung angeben"
    exit 1
fi

# Extract basename without extension
INPUT="$1"
BASENAME=$(echo "$INPUT" | sed 's/\.[^.]*$//')

echo -e "${BLUE}🔍 Suche Dokument: ${BASENAME}${NC}"
echo ""

# Check if files exist in knowledge_base_final
KB_DE="knowledge_base_final/${BASENAME}_de.md"
KB_EN="knowledge_base_final/${BASENAME}_en.md"
INPUT_FILE=""

# Find input file
for ext in pdf docx jpg png JPG PNG; do
    if [ -f "inputs/${BASENAME}.${ext}" ]; then
        INPUT_FILE="inputs/${BASENAME}.${ext}"
        break
    fi
done

# Show what will be deleted
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${YELLOW}📋 Zu löschende Dateien:${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

FILES_TO_DELETE=()

if [ -f "$KB_DE" ]; then
    echo -e "  ✅ ${KB_DE}"
    FILES_TO_DELETE+=("$KB_DE")
else
    echo -e "  ${YELLOW}⚠️  Nicht gefunden: ${KB_DE}${NC}"
fi

if [ -f "$KB_EN" ]; then
    echo -e "  ✅ ${KB_EN}"
    FILES_TO_DELETE+=("$KB_EN")
else
    echo -e "  ${YELLOW}⚠️  Nicht gefunden: ${KB_EN}${NC}"
fi

if [ -n "$INPUT_FILE" ]; then
    echo -e "  ${BLUE}📄 Original: ${INPUT_FILE}${NC}"
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Exit if no files found
if [ ${#FILES_TO_DELETE[@]} -eq 0 ]; then
    echo ""
    echo -e "${YELLOW}✅ Dokument nicht in Knowledge Base gefunden.${NC}"
    echo -e "   Nichts zu tun."
    echo ""
    exit 0
fi

# Confirmation
echo ""
echo -e "${RED}⚠️  WARNUNG: Diese Aktion kann nicht rückgängig gemacht werden!${NC}"
echo ""
echo -e "${YELLOW}Auswirkungen:${NC}"
echo -e "  ❌ Bot kennt dieses Dokument NICHT mehr"
echo -e "  ❌ Alle Informationen aus diesem Dokument sind weg"
echo -e "  ✅ Kann durch erneute Verarbeitung wiederhergestellt werden"
echo ""

read -p "Wirklich löschen? (j/n): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Jj]$ ]]; then
    echo -e "${YELLOW}❌ Abgebrochen - Keine Dateien gelöscht${NC}"
    echo ""
    exit 1
fi

# Delete from knowledge_base_final
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${YELLOW}🗑️  Lösche aus Knowledge Base...${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

for file in "${FILES_TO_DELETE[@]}"; do
    if [ -f "$file" ]; then
        rm "$file"
        echo -e "${GREEN}✅ Gelöscht: ${file}${NC}"
    fi
done

# Ask about input file
if [ -n "$INPUT_FILE" ]; then
    echo ""
    read -p "Auch Original aus inputs/ löschen? (j/n): " -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^[Jj]$ ]]; then
        rm "$INPUT_FILE"
        echo -e "${GREEN}✅ Gelöscht: ${INPUT_FILE}${NC}"
    else
        echo -e "${BLUE}⏭️  Original behalten: ${INPUT_FILE}${NC}"
    fi
fi

# Git commit
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${YELLOW}📦 Git Deployment${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

git status

echo ""
read -p "Git commit & push durchführen? (j/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Jj]$ ]]; then
    git add knowledge_base_final/
    
    if [ -n "$INPUT_FILE" ] && [ ! -f "$INPUT_FILE" ]; then
        git add inputs/
    fi
    
    COMMIT_MSG="Remove: ${BASENAME} aus Knowledge Base entfernt"
    git commit -m "$COMMIT_MSG"
    git push origin main
    
    echo ""
    echo -e "${GREEN}✅ Git Deployment erfolgreich!${NC}"
    echo ""
    echo -e "${BLUE}🌐 Render deployed automatisch in ~3-4 Minuten${NC}"
    echo -e "   Bot wird dieses Dokument dann NICHT mehr kennen.${NC}"
else
    echo ""
    echo -e "${YELLOW}⏭️  Git-Deployment übersprungen${NC}"
    echo -e "   Du kannst es später manuell machen mit:"
    echo -e "   ${BLUE}git add knowledge_base_final/ && git commit -m 'Remove KB' && git push${NC}"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}✅ CLEANUP ABGESCHLOSSEN!${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Show remaining KB size
REMAINING=$(ls knowledge_base_final/*.md 2>/dev/null | wc -l)
echo -e "${BLUE}📊 Verbleibende Knowledge Base: ${REMAINING} Dateien${NC}"
echo ""
