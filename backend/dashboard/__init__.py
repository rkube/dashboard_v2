# Begin file backend/views/__init__.py

from flask import Blueprint

# we name the blueprint dashboard
# the template folder is called templates. File names passed to render_template are relative to this path
dashboard = Blueprint("dashboard", __name__, template_folder="templates")

from . import dashboard_routes


# End file __init__.py