# PythonAnywhere WSGI configuration file
#
# HOW TO USE:
# 1. Go to pythonanywhere.com -> Web tab -> Add new web app
# 2. Choose "Manual configuration" -> Python 3.11
# 3. In the WSGI configuration file section, replace the content
#    with this file's content (updating the path below)
# 4. Set the path to: /home/YOUR_USERNAME/MathPhiCafe
#
# Replace YOUR_USERNAME with your PythonAnywhere username everywhere below.

import sys
import os

# Add project directory to path
project_home = '/home/YOUR_USERNAME/MathPhiCafe'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variables
os.environ['SECRET_KEY'] = 'change-this-to-a-random-secret-key-in-production'

# Import Flask app
from run import app as application  # noqa
