#!/bin/bash
#
# SpinThatShit Installer
# ======================
# Installs the SpinThatShit orchestration system
#

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color
BOLD='\033[1m'

echo ""
echo -e "${CYAN}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║${NC}       ${BOLD}🔄 SpinThatShit Installer 🔄${NC}                        ${CYAN}║${NC}"
echo -e "${CYAN}║${NC}       AI Agent Orchestration System                      ${CYAN}║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""

# Detect OS
OS="unknown"
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
    echo -e "${GREEN}✓${NC} Detekován macOS"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
    echo -e "${GREEN}✓${NC} Detekován Linux"
else
    echo -e "${RED}✗${NC} Nepodporovaný OS: $OSTYPE"
    exit 1
fi

# Check Python
echo -e "\n${BLUE}Kontroluji závislosti...${NC}"

if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
    echo -e "${GREEN}✓${NC} Python ${PYTHON_VERSION}"
else
    echo -e "${RED}✗${NC} Python3 není nainstalován"
    echo -e "  Prosím nainstalujte Python 3.8+"
    exit 1
fi

# Check Claude Code CLI
if command -v claude &> /dev/null; then
    echo -e "${GREEN}✓${NC} Claude Code CLI nalezen"
else
    echo -e "${YELLOW}!${NC} Claude Code CLI není nainstalován"
    echo -e "  Instalace: npm install -g @anthropic-ai/claude-code"
    read -p "  Chcete pokračovat bez něj? [y/N]: " continue_without
    if [[ ! "$continue_without" =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check Git
if command -v git &> /dev/null; then
    echo -e "${GREEN}✓${NC} Git nalezen"
else
    echo -e "${RED}✗${NC} Git není nainstalován"
    exit 1
fi

# Installation directory
INSTALL_DIR="$HOME/.spinthatshit"
BIN_DIR="$HOME/.local/bin"

echo -e "\n${BLUE}Instaluji do: ${INSTALL_DIR}${NC}"

# Create directories
mkdir -p "$INSTALL_DIR"
mkdir -p "$BIN_DIR"
mkdir -p "$INSTALL_DIR/prompts"
mkdir -p "$INSTALL_DIR/templates"
mkdir -p "$INSTALL_DIR/logs"

# Get script directory (where installer is)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Copy main script
if [[ -f "$SCRIPT_DIR/spin.py" ]]; then
    cp "$SCRIPT_DIR/spin.py" "$INSTALL_DIR/spin.py"
    echo -e "${GREEN}✓${NC} Hlavní script zkopírován"
else
    echo -e "${RED}✗${NC} spin.py nenalezen v $SCRIPT_DIR"
    exit 1
fi

# Copy prompts if exist
if [[ -d "$SCRIPT_DIR/prompts" ]]; then
    cp -r "$SCRIPT_DIR/prompts/"* "$INSTALL_DIR/prompts/" 2>/dev/null || true
    echo -e "${GREEN}✓${NC} Prompty zkopírovány"
fi

# Copy templates if exist
if [[ -d "$SCRIPT_DIR/templates" ]]; then
    cp -r "$SCRIPT_DIR/templates/"* "$INSTALL_DIR/templates/" 2>/dev/null || true
    echo -e "${GREEN}✓${NC} Šablony zkopírovány"
fi

# Create the main executable
cat > "$BIN_DIR/spinthatshit" << 'SCRIPT'
#!/bin/bash
# SpinThatShit launcher
exec python3 "$HOME/.spinthatshit/spin.py" "$@"
SCRIPT

chmod +x "$BIN_DIR/spinthatshit"
echo -e "${GREEN}✓${NC} Příkaz 'spinthatshit' vytvořen"

# Create shorter alias
cat > "$BIN_DIR/sts" << 'SCRIPT'
#!/bin/bash
# SpinThatShit shortcut
exec python3 "$HOME/.spinthatshit/spin.py" "$@"
SCRIPT

chmod +x "$BIN_DIR/sts"
echo -e "${GREEN}✓${NC} Zkratka 'sts' vytvořena"

# Add to PATH if needed
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo ""
    echo -e "${YELLOW}!${NC} $BIN_DIR není ve vašem PATH"
    echo ""
    
    # Detect shell
    SHELL_NAME=$(basename "$SHELL")
    case "$SHELL_NAME" in
        bash)
            RC_FILE="$HOME/.bashrc"
            ;;
        zsh)
            RC_FILE="$HOME/.zshrc"
            ;;
        *)
            RC_FILE="$HOME/.profile"
            ;;
    esac
    
    read -p "  Přidat do $RC_FILE? [Y/n]: " add_path
    if [[ ! "$add_path" =~ ^[Nn]$ ]]; then
        echo "" >> "$RC_FILE"
        echo "# SpinThatShit" >> "$RC_FILE"
        echo "export PATH=\"\$HOME/.local/bin:\$PATH\"" >> "$RC_FILE"
        echo -e "${GREEN}✓${NC} PATH aktualizován v $RC_FILE"
        echo -e "${YELLOW}!${NC} Spusťte: source $RC_FILE"
    fi
fi

# Create config template
cat > "$INSTALL_DIR/config.json" << 'CONFIG'
{
    "version": "1.0.0",
    "context_limit_percent": 50,
    "max_retries": 3,
    "agent_timeout_minutes": 30,
    "auto_push": true,
    "language": {
        "user": "cs",
        "system": "en"
    },
    "agents": {
        "workflow_order": [
            "planner",
            "designer", 
            "engineer",
            "developer",
            "reviewer",
            "tester",
            "supervisor"
        ],
        "enabled": {
            "planner": true,
            "designer": true,
            "engineer": true,
            "developer": true,
            "reviewer": true,
            "tester": true,
            "supervisor": true,
            "evolver": true
        }
    }
}
CONFIG

echo -e "${GREEN}✓${NC} Výchozí konfigurace vytvořena"

# Create uninstaller
cat > "$INSTALL_DIR/uninstall.sh" << 'UNINSTALL'
#!/bin/bash
echo "Odinstalovávám SpinThatShit..."
rm -rf "$HOME/.spinthatshit"
rm -f "$HOME/.local/bin/spinthatshit"
rm -f "$HOME/.local/bin/sts"
echo "Hotovo. Můžete odstranit PATH z vašeho shell RC souboru."
UNINSTALL
chmod +x "$INSTALL_DIR/uninstall.sh"

# Done!
echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║${NC}              ${BOLD}✅ Instalace dokončena! ✅${NC}                   ${GREEN}║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "Použití:"
echo -e "  ${CYAN}spinthatshit${NC}           - Spustit interaktivně"
echo -e "  ${CYAN}sts${NC}                    - Zkratka"
echo -e "  ${CYAN}spinthatshit --help${NC}    - Nápověda"
echo -e "  ${CYAN}spinthatshit --resume${NC}  - Pokračovat od posledního stavu"
echo ""
echo -e "Odinstalace:"
echo -e "  ${CYAN}~/.spinthatshit/uninstall.sh${NC}"
echo ""
echo -e "${YELLOW}Tip: Pro nový terminál spusťte: source ~/.bashrc (nebo ~/.zshrc)${NC}"
echo ""
