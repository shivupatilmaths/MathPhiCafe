# ============================================================
#  PythonAnywhere WSGI config for MathPhiCafe  (manual template)
#
#  The setup script (pythonanywhere_setup.sh) generates a
#  ready-to-use version of this file called
#  pythonanywhere_wsgi_live.py with YOUR username and a
#  random SECRET_KEY already filled in.
#
#  If you prefer to fill it in manually, use this template:
#  1. Replace YOUR_USERNAME with your PythonAnywhere username
#  2. Generate a secret key:
#       python3 -c "import secrets; print(secrets.token_hex(32))"
#  3. Paste into the WSGI file shown in the Web tab
#
#  NOTE: The virtualenv is activated automatically by PythonAnywhere
#  when you set the "Virtualenv" field in the Web tab.
#  You do NOT need activate_this.py here.
# ============================================================

import sys
import os

project_home = '/home/YOUR_USERNAME/MathPhiCafe'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

os.environ['SECRET_KEY'] = 'REPLACE_WITH_OUTPUT_OF_secrets.token_hex(32)'

from run import app as application  # noqa
