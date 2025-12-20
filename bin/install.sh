#!/bin/bash
set -e

TARGET="${1:-$HOME/.spinthatshit}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "🌀 Installing SpinThatShit to $TARGET"

mkdir -p "$TARGET"
cp -r "$SCRIPT_DIR"/* "$TARGET/"
cp -r "$SCRIPT_DIR"/.[^.]* "$TARGET/" 2>/dev/null || true

mkdir -p "$TARGET/bin"
cat > "$TARGET/bin/spinthatshit" << EOF
#!/bin/bash
python3 "$TARGET/spin.py" "\$@"
EOF
chmod +x "$TARGET/bin/spinthatshit"

# Add to PATH
SHELL_RC="$HOME/.zshrc"
[[ ! -f "$SHELL_RC" ]] && SHELL_RC="$HOME/.bashrc"

if [[ -f "$SHELL_RC" ]] && ! grep -q "spinthatshit" "$SHELL_RC"; then
    echo "" >> "$SHELL_RC"
    echo "# SpinThatShit" >> "$SHELL_RC"
    echo "export PATH=\"\$PATH:$TARGET/bin\"" >> "$SHELL_RC"
fi

echo "✅ Installation complete!"
echo "   Restart terminal or: source $SHELL_RC"
