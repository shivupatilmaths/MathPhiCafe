#!/bin/bash
# =============================================================
#  MathPhiCafe - PythonAnywhere One-Time Setup Script
#  Run this from PythonAnywhere's Bash console:
#  bash pythonanywhere_setup.sh YOUR_USERNAME
# =============================================================

set -e

USERNAME="${1:-$(whoami)}"
PROJECT_DIR="/home/$USERNAME/MathPhiCafe"
VENV_DIR="/home/$USERNAME/.virtualenvs/mathphicafe"
REPO_URL="https://github.com/shivupatilmaths/MathPhiCafe.git"

echo "========================================"
echo " MathPhiCafe PythonAnywhere Setup"
echo " Username : $USERNAME"
echo " Project  : $PROJECT_DIR"
echo " Venv     : $VENV_DIR"
echo "========================================"

# 1. Clone or update repo
if [ -d "$PROJECT_DIR" ]; then
    echo "[1/6] Updating existing repo..."
    git -C "$PROJECT_DIR" pull origin master
else
    echo "[1/6] Cloning repo..."
    git clone "$REPO_URL" "$PROJECT_DIR"
fi

# 2. Create virtualenv
echo "[2/6] Setting up Python virtualenv..."
python3.11 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"

# 3. Install dependencies
echo "[3/6] Installing dependencies..."
pip install --upgrade pip --quiet
pip install -r "$PROJECT_DIR/requirements.txt" --quiet

# 4. Create upload directories
echo "[4/6] Creating upload directories..."
mkdir -p "$PROJECT_DIR/app/static/uploads/gallery"
mkdir -p "$PROJECT_DIR/app/static/uploads/notes"
mkdir -p "$PROJECT_DIR/app/static/uploads/avatars"
mkdir -p "$PROJECT_DIR/app/static/uploads/thumbnails"
mkdir -p "$PROJECT_DIR/instance"

# 5. Seed database
echo "[5/6] Seeding database..."
cd "$PROJECT_DIR"
python seed.py

# 6. Generate WSGI file for this user
echo "[6/6] Writing WSGI config file..."
cat > "$PROJECT_DIR/pythonanywhere_wsgi_live.py" <<WSGI
import sys
import os

project_home = '/home/$USERNAME/MathPhiCafe'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

os.environ['SECRET_KEY'] = '$(python3 -c "import secrets; print(secrets.token_hex(32))")'

activate_this = '/home/$USERNAME/.virtualenvs/mathphicafe/bin/activate_this.py'
with open(activate_this) as f:
    exec(f.read(), {'__file__': activate_this})

from run import app as application  # noqa
WSGI

echo ""
echo "========================================"
echo " SETUP COMPLETE!"
echo "========================================"
echo ""
echo "NEXT STEPS (do these in your browser):"
echo ""
echo "1. Go to: https://www.pythonanywhere.com/user/$USERNAME/webapps/add/"
echo "   -> Choose 'Manual configuration' -> Python 3.11 -> Next"
echo ""
echo "2. In the Web tab, set:"
echo "   Source code    : $PROJECT_DIR"
echo "   Working dir    : $PROJECT_DIR"
echo "   Virtualenv     : $VENV_DIR"
echo ""
echo "3. Click 'WSGI configuration file' link, then REPLACE all its"
echo "   content with the content of:"
echo "   $PROJECT_DIR/pythonanywhere_wsgi_live.py"
echo ""
echo "4. Click the green 'Reload $USERNAME.pythonanywhere.com' button"
echo ""
echo "5. Your site is live at: https://$USERNAME.pythonanywhere.com"
echo ""
echo "   Admin login -> username: admin | password: admin123"
echo "   (Change the password immediately after logging in!)"
echo ""
