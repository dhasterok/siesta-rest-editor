#!/usr/bin/env bash
# Build "dist/reST Editor.app", a standalone macOS application.
#
# Usage:  ./build_mac.sh            (uses .venv/bin/python if present)
#         PYTHON=/path/to/python ./build_mac.sh
#
# The Python used must have the project's dependencies installed
# (pip install -r requirements-dev.txt); PyInstaller is installed if missing.
set -euo pipefail
cd "$(dirname "$0")"

PYTHON="${PYTHON:-}"
if [[ -z "$PYTHON" ]]; then
    if [[ -x .venv/bin/python ]]; then PYTHON=.venv/bin/python; else PYTHON=python3; fi
fi
echo "Using $("$PYTHON" -c 'import sys; print(sys.executable, sys.version.split()[0])')"

"$PYTHON" -c "import PyInstaller" 2>/dev/null || "$PYTHON" -m pip install "pyinstaller>=6.10"

# --- App icon: render siesta2.svg into an .icns (Dock / Finder icon) ----------
ICON_SVG=src/siesta/icons/siesta2.svg
ICON_DIR=build/icon
ICONSET="$ICON_DIR/reSTEdit.iconset"
if [[ ! -f "$ICON_DIR/reSTEdit.icns" || "$ICON_SVG" -nt "$ICON_DIR/reSTEdit.icns" ]]; then
    echo "Generating app icon from $ICON_SVG..."
    rm -rf "$ICONSET"; mkdir -p "$ICONSET"
    QT_QPA_PLATFORM=offscreen "$PYTHON" - "$ICONSET" "$ICON_SVG" <<'EOF'
import sys
from pathlib import Path
from PyQt6.QtGui import QGuiApplication, QImage, QPainter
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtCore import QRectF, Qt

app = QGuiApplication(sys.argv)
renderer = QSvgRenderer(sys.argv[2])
out = Path(sys.argv[1])
for size in (16, 32, 128, 256, 512):
    for scale in (1, 2):
        px = size * scale
        img = QImage(px, px, QImage.Format.Format_ARGB32)
        img.fill(Qt.GlobalColor.transparent)
        p = QPainter(img)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        # the SVG supplies its own rounded background tile, so draw it full-size
        renderer.render(p, QRectF(0, 0, px, px))
        p.end()
        suffix = "@2x" if scale == 2 else ""
        img.save(str(out / f"icon_{size}x{size}{suffix}.png"))
EOF
    iconutil -c icns "$ICONSET" -o "$ICON_DIR/reSTEdit.icns"
fi

# --- Build -------------------------------------------------------------------
"$PYTHON" -m PyInstaller --noconfirm --clean reSTEdit.spec

echo
echo "Built: dist/reST Editor.app"
echo "Run it with:  open \"dist/reST Editor.app\""
