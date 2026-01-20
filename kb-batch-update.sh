#!/bin/bash
###############################################################################
# kb-batch-update.sh - Process ALL new documents in inputs/ folder
# 
# Usage: ./kb-batch-update.sh
#
# This script:
# 1. Finds all documents in inputs/ that are NOT yet in knowledge_base_final/
# 2. Processes them one by one (Marker + GPT-5.2)
# 3. Creates one Git commit for all updates
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
echo -e "${GREEN}🔄 Batch-Verarbeitung: Alle neuen Dokumente${NC}"
echo "========================================================================"
echo ""

# Find all documents in inputs/
INPUT_FILES=(inputs/*.pdf inputs/*.docx inputs/*.jpg inputs/*.png inputs/*.JPG inputs/*.PNG 2>/dev/null)

# Filter: Only new documents (not yet in knowledge_base_final)
NEW_FILES=()
PROCESSED=0
SKIPPED=0

echo -e "${BLUE}📋 Prüfe inputs/ Ordner...${NC}"
echo ""

for file in "${INPUT_FILES[@]}"; do
    # Skip if glob didn't match anything
    if [ ! -f "$file" ]; then
        continue
    fi
    
    # Extract basename without extension
    basename=$(basename "$file" | sed 's/\.[^.]*$//')
    
    # Check if already processed (both _de.md and _en.md exist)
    if [ -f "knowledge_base_final/${basename}_de.md" ] && [ -f "knowledge_base_final/${basename}_en.md" ]; then
        echo -e "${YELLOW}⏭️  Überspringe (bereits verarbeitet): ${basename}${NC}"
        ((SKIPPED++))
    else
        echo -e "${GREEN}✅ Neu gefunden: ${basename}${NC}"
        NEW_FILES+=("$file")
    fi
done

echo ""
echo "========================================================================"
echo -e "${BLUE}📊 Status:${NC}"
echo -e "  Neu zu verarbeiten: ${GREEN}${#NEW_FILES[@]}${NC}"
echo -e "  Bereits verarbeitet: ${YELLOW}${SKIPPED}${NC}"
echo "========================================================================"
echo ""

# Exit if no new files
if [ ${#NEW_FILES[@]} -eq 0 ]; then
    echo -e "${YELLOW}✅ Keine neuen Dokumente gefunden. Alles ist aktuell!${NC}"
    echo ""
    exit 0
fi

# Ask for confirmation
echo -e "${YELLOW}Möchtest du diese ${#NEW_FILES[@]} Dokument(e) verarbeiten?${NC}"
read -p "Fortfahren? (j/n): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Jj]$ ]]; then
    echo -e "${RED}❌ Abgebrochen${NC}"
    exit 1
fi

echo ""
echo "========================================================================"
echo -e "${YELLOW}🚀 Starte Verarbeitung...${NC}"
echo "========================================================================"
echo ""

# Process each new file
for file in "${NEW_FILES[@]}"; do
    basename=$(basename "$file")
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo -e "${BLUE}📄 Verarbeite ($((PROCESSED+1))/${#NEW_FILES[@]}): ${basename}${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    # Run update script
    if ./update_knowledge.sh "$file"; then
        echo -e "${GREEN}✅ Erfolgreich: ${basename}${NC}"
        ((PROCESSED++))
    else
        echo -e "${RED}❌ Fehler bei: ${basename}${NC}"
        echo -e "${YELLOW}Möchtest du trotzdem fortfahren?${NC}"
        read -p "(j/n): " -n 1 -r
        echo ""
        if [[ ! $REPLY =~ ^[Jj]$ ]]; then
            echo -e "${RED}❌ Abgebrochen${NC}"
            exit 1
        fi
    fi
done

echo ""
echo "========================================================================"
echo -e "${GREEN}✨ Verarbeitung abgeschlossen!${NC}"
echo "========================================================================"
echo ""
echo -e "${BLUE}📊 Ergebnis:${NC}"
echo -e "  Erfolgreich verarbeitet: ${GREEN}${PROCESSED}${NC}"
echo ""

# Git commit
if [ $PROCESSED -gt 0 ]; then
    echo "========================================================================"
    echo -e "${YELLOW}📦 Git Deployment${NC}"
    echo "========================================================================"
    echo ""
    
    # Show changes
    git status
    
    echo ""
    read -p "Git commit & push durchführen? (j/n): " -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^[Jj]$ ]]; then
        # Add all new knowledge base files
        git add knowledge_base_final/
        
        # Commit
        if [ $PROCESSED -eq 1 ]; then
            COMMIT_MSG="Add: 1 neues Dokument zur Knowledge Base"
        else
            COMMIT_MSG="Add: ${PROCESSED} neue Dokumente zur Knowledge Base"
        fi
        
        git commit -m "$COMMIT_MSG"
        git push origin main
        
        echo ""
        echo -e "${GREEN}✅ Git Deployment erfolgreich!${NC}"
        echo ""
        echo -e "${BLUE}🌐 Render deployed automatisch in ~3-4 Minuten${NC}"
    else
        echo ""
        echo -e "${YELLOW}⏭️  Git-Deployment übersprungen${NC}"
        echo -e "   Du kannst es später manuell machen mit:"
        echo -e "   ${BLUE}git add knowledge_base_final/ && git commit -m 'Update KB' && git push${NC}"
    fi
fi

echo ""
echo "========================================================================"
echo -e "${GREEN}🎉 FERTIG!${NC}"
echo "========================================================================"
echo ""
