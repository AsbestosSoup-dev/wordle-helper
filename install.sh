#!/usr/bin/env bash
set -euo pipefail

# Install script for Wordle Helper CLI
# - Creates a local virtual environment in .venv
# - Upgrades pip
# - Installs dependencies from requirements.txt (if any)
# Usage: bash install.sh

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

# Choose python
if command -v python3 >/dev/null 2>&1; then
  PY=python3
elif command -v python >/dev/null 2>&1; then
  PY=python
else
  echo "Error: Python is not installed." >&2
  exit 1
fi

# Show version
"$PY" -c 'import sys; print(f"Using Python {sys.version.split()[0]}")'

# Create venv
if [ ! -d ".venv" ]; then
  echo "Creating virtual environment in .venv ..."
  "$PY" -m venv .venv
else
  echo ".venv already exists — reusing it."
fi

# Use venv's python/pip directly (no need to activate)
VENV_PY="./.venv/bin/python"
VENV_PIP="./.venv/bin/pip"

if [ ! -x "$VENV_PY" ]; then
  echo "Error: venv python not found at $VENV_PY" >&2
  exit 1
fi

echo "Upgrading pip ..."
"$VENV_PIP" install --upgrade pip

# Install dependencies if requirements.txt has any non-comment, non-empty lines
if [ -f "requirements.txt" ] && grep -qE '^[[:space:]]*[^#[:space:]]' requirements.txt; then
  echo "Installing dependencies from requirements.txt ..."
  "$VENV_PIP" install -r requirements.txt
else
  echo "No runtime dependencies to install."
fi

# Create a convenience runner
cat > run.sh <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "$DIR/.venv/bin/python" "$DIR/main.py"
EOF

chmod +x run.sh

echo "----------------------------------------"
echo "Setup complete."
echo "Run the app with:"
echo "  bash run.sh"
echo ""
echo "Or manually:"
echo "  source .venv/bin/activate && python main.py"
echo "----------------------------------------"
