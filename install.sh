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
    echo -e "${GREEN}✓${NC} Detected macOS"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
    echo -e "${GREEN}✓${NC} Detected Linux"
else
    echo -e "${RED}✗${NC} Unsupported OS: $OSTYPE"
    exit 1
fi

# Check Python
echo -e "\n${BLUE}Checking dependencies...${NC}"

if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
    echo -e "${GREEN}✓${NC} Python ${PYTHON_VERSION}"
else
    echo -e "${RED}✗${NC} Python3 is not installed"
    echo -e "  Please install Python 3.8+"
    exit 1
fi

# Check Claude Code CLI
if command -v claude &> /dev/null; then
    echo -e "${GREEN}✓${NC} Claude Code CLI found"
else
    echo -e "${YELLOW}!${NC} Claude Code CLI is not installed"
    echo -e "  Install: npm install -g @anthropic-ai/claude-code"
    read -p "  Continue without it? [y/N]: " continue_without
    if [[ ! "$continue_without" =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check Git
if command -v git &> /dev/null; then
    echo -e "${GREEN}✓${NC} Git found"
else
    echo -e "${RED}✗${NC} Git is not installed"
    exit 1
fi

# Installation directory
INSTALL_DIR="$HOME/.spinthatshit"
BIN_DIR="$HOME/.local/bin"

echo -e "\n${BLUE}Installing to: ${INSTALL_DIR}${NC}"

# Create directories
mkdir -p "$INSTALL_DIR"
mkdir -p "$BIN_DIR"
mkdir -p "$INSTALL_DIR/prompts"
mkdir -p "$INSTALL_DIR/templates"
mkdir -p "$INSTALL_DIR/logs"
mkdir -p "$INSTALL_DIR/i18n/locales"

# Get script directory (where installer is)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Copy main script
if [[ -f "$SCRIPT_DIR/spin.py" ]]; then
    cp "$SCRIPT_DIR/spin.py" "$INSTALL_DIR/spin.py"
    echo -e "${GREEN}✓${NC} Main script copied"
else
    echo -e "${RED}✗${NC} spin.py not found in $SCRIPT_DIR"
    exit 1
fi

# Copy i18n module
if [[ -d "$SCRIPT_DIR/i18n" ]]; then
    cp -r "$SCRIPT_DIR/i18n/"* "$INSTALL_DIR/i18n/" 2>/dev/null || true
    echo -e "${GREEN}✓${NC} i18n translations copied (32 languages)"
else
    echo -e "${YELLOW}!${NC} i18n directory not found - translations will not be available"
fi

# Copy prompts if exist
if [[ -d "$SCRIPT_DIR/prompts" ]]; then
    cp -r "$SCRIPT_DIR/prompts/"* "$INSTALL_DIR/prompts/" 2>/dev/null || true
    echo -e "${GREEN}✓${NC} Prompts copied"
fi

# Copy templates if exist
if [[ -d "$SCRIPT_DIR/templates" ]]; then
    cp -r "$SCRIPT_DIR/templates/"* "$INSTALL_DIR/templates/" 2>/dev/null || true
    echo -e "${GREEN}✓${NC} Templates copied"
fi

# Create the main executable
cat > "$BIN_DIR/spinthatshit" << 'SCRIPT'
#!/bin/bash
# SpinThatShit launcher
exec python3 "$HOME/.spinthatshit/spin.py" "$@"
SCRIPT

chmod +x "$BIN_DIR/spinthatshit"
echo -e "${GREEN}✓${NC} Command 'spinthatshit' created"

# Create shorter alias
cat > "$BIN_DIR/sts" << 'SCRIPT'
#!/bin/bash
# SpinThatShit shortcut
exec python3 "$HOME/.spinthatshit/spin.py" "$@"
SCRIPT

chmod +x "$BIN_DIR/sts"
echo -e "${GREEN}✓${NC} Shortcut 'sts' created"

# Add to PATH if needed
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo ""
    echo -e "${YELLOW}!${NC} $BIN_DIR is not in your PATH"
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

    read -p "  Add to $RC_FILE? [Y/n]: " add_path
    if [[ ! "$add_path" =~ ^[Nn]$ ]]; then
        echo "" >> "$RC_FILE"
        echo "# SpinThatShit" >> "$RC_FILE"
        echo "export PATH=\"\$HOME/.local/bin:\$PATH\"" >> "$RC_FILE"
        echo -e "${GREEN}✓${NC} PATH updated in $RC_FILE"
        echo -e "${YELLOW}!${NC} Run: source $RC_FILE"
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

echo -e "${GREEN}✓${NC} Default configuration created"

# Create uninstaller
cat > "$INSTALL_DIR/uninstall.sh" << 'UNINSTALL'
#!/bin/bash
echo "Uninstalling SpinThatShit..."
rm -rf "$HOME/.spinthatshit"
rm -f "$HOME/.local/bin/spinthatshit"
rm -f "$HOME/.local/bin/sts"
echo "Done. You may remove PATH from your shell RC file."
UNINSTALL
chmod +x "$INSTALL_DIR/uninstall.sh"

# Done!
echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║${NC}            ${BOLD}✅ Installation Complete! ✅${NC}                  ${GREEN}║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${CYAN}🌍 SpinThatShit supports 32 languages!${NC}"
echo -e "   On first run, you'll be able to select your language."
echo ""
echo -e "Usage:"
echo -e "  ${CYAN}spinthatshit${NC}              - Run interactively"
echo -e "  ${CYAN}sts${NC}                       - Shortcut"
echo -e "  ${CYAN}spinthatshit --help${NC}       - Show help"
echo -e "  ${CYAN}spinthatshit --lang cs${NC}    - Set language (e.g., cs, en, es)"
echo -e "  ${CYAN}spinthatshit --resume${NC}     - Resume from last state"
echo ""
echo -e "Uninstall:"
echo -e "  ${CYAN}~/.spinthatshit/uninstall.sh${NC}"
echo ""
echo -e "${YELLOW}Tip: For a new terminal run: source ~/.bashrc (or ~/.zshrc)${NC}"
echo ""
