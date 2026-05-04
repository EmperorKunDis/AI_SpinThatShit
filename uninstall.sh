#!/bin/bash
echo "Uninstalling SpinThatShit..."
rm -rf "$HOME/.spinthatshit"
rm -f "$HOME/.local/bin/spinthatshit"
rm -f "$HOME/.local/bin/sts"
echo "Done. You may remove PATH from your shell RC file."
