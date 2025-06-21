#!/usr/bin/env bash
# -----------------------------------------------------------
# Password Strength Analyzer & Word-list Generator – Linux installer
# Re-written 2025-06-14 to fix “neither setup.py nor pyproject.toml found”
# -----------------------------------------------------------
set -e  # stop on first error

echo "=================================================="
echo " Password Strength Analyzer & Word-list Generator "
echo " Ubuntu / Debian Installer"
echo "=================================================="
echo

# ----- 1. locate project root ------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"     # …/PasswordTool/scripts
PROJECT_ROOT="$(realpath "${SCRIPT_DIR}/..")"                  # …/PasswordTool
echo "Project root: ${PROJECT_ROOT}"
cd "${PROJECT_ROOT}"

# ----- 2. create / activate virtual-env --------------------------------------
echo -e "\nCreating virtual environment (.venv)…"
python3 -m venv .venv
source .venv/bin/activate

# ----- 3. install packages ---------------------------------------------------
echo -e "\nUpgrading pip / build backend…"
python -m pip install --upgrade pip setuptools wheel

echo -e "\nInstalling project in editable mode…"
# editable install **must** point at the real project root
python -m pip install -e "${PROJECT_ROOT}"

echo -e "\nInstalling extra requirements…"
python -m pip install -r requirements.txt

# ----- 4. desktop entry ------------------------------------------------------
echo -e "\nCreating desktop shortcut…"

DESKTOP_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/applications"
mkdir -p "${DESKTOP_DIR}"                         # ← ensures the folder exists
DESKTOP_FILE="${DESKTOP_DIR}/pass_tool.desktop"

cat > "${DESKTOP_FILE}" <<EOF
[Desktop Entry]
Name=Password Strength Analyzer
Comment=Analyse password strength and generate word-lists
Exec=${PROJECT_ROOT}/.venv/bin/python -m pass_tool.gui
Terminal=false
Type=Application
Categories=Utility;
EOF

chmod +x "${DESKTOP_FILE}"
update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true

chmod +x "${DESKTOP_FILE}"

echo
echo "✅  Installation finished."
echo "   You can launch the program from your application menu"
echo "   or run:  ${PROJECT_ROOT}/.venv/bin/python -m pass_tool.gui"
