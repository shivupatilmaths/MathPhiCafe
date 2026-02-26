# ============================================================
#  PythonAnywhere WSGI configuration for MathPhiCafe
#
#  HOW TO USE:
#  Copy this file's content into your PythonAnywhere WSGI file.
#  The WSGI file path looks like:
#    /var/www/USERNAME_pythonanywhere_com_wsgi.py
#
#  Replace YOUR_USERNAME with your PythonAnywhere username below.
# ============================================================

import sys
import os

# ---- 1. Set your username here ----
USERNAME = 'YOUR_USERNAME'
# -----------------------------------

project_home = f'/home/{USERNAME}/MathPhiCafe'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Activate the virtualenv
activate_this = f'/home/{USERNAME}/.virtualenvs/mathphicafe/bin/activate_this.py'
with open(activate_this) as f:
    exec(f.read(), {'__file__': activate_this})

# Set a strong secret key (generate one at: python3 -c "import secrets; print(secrets.token_hex(32))")
os.environ['SECRET_KEY'] = 'REPLACE_WITH_A_RANDOM_64_CHAR_SECRET'

# Import Flask app
from run import app as application  # noqa
