#!/bin/bash
###############################################################################
# start_flask.sh - Flask Development Server Starter
# 
# Verwendung:
#   ./start_flask.sh
#
# Dieses Script:
#   1. Aktiviert automatisch die richtige Virtual Environment (.venv)
#   2. Prüft ob Port 5001 frei ist (stoppt alte Flask-Instanzen)
#   3. Startet Flask auf Port 5001
#   4. Lädt .flaskenv automatisch
###############################################################################

set -e

# Farben
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

echo ""
echo "========================================================================"
echo -e "${GREEN}🚀 Flask Development Server Starter${NC}"
echo "========================================================================"
echo ""

# Prüfe, ob .venv existiert
if [ ! -d ".venv" ]; then
    echo -e "${RED}❌ Fehler: .venv nicht gefunden!${NC}"
    echo "Bitte erstelle zuerst die Virtual Environment:"
    echo "  python3 -m venv .venv"
    echo "  source .venv/bin/activate"
    echo "  pip install -r requirements.txt"
    exit 1
fi

# Stoppe alte Flask-Prozesse auf Port 5001
echo -e "${YELLOW}🔍 Prüfe Port 5001...${NC}"
PID=$(lsof -t -i:5001 2>/dev/null || true)

if [ ! -z "$PID" ]; then
    echo -e "${YELLOW}⚠️  Port 5001 ist belegt (PID: $PID). Stoppe alten Prozess...${NC}"
    kill $PID 2>/dev/null || true
    sleep 2
    echo -e "${GREEN}✅ Port 5001 ist jetzt frei${NC}"
else
    echo -e "${GREEN}✅ Port 5001 ist frei${NC}"
fi

echo ""

# Aktiviere .venv
echo -e "${GREEN}✅ Aktiviere Flask Environment (.venv)${NC}"
source .venv/bin/activate

echo ""
echo "========================================================================"
echo -e "${GREEN}🌐 Starte Flask auf http://localhost:5001${NC}"
echo "========================================================================"
echo ""
echo "Drücke STRG+C zum Beenden"
echo ""

# Starte Flask (lädt .flaskenv automatisch)
flask run
