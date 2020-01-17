# Begin file backend/views/__init__.py

from flask import Blueprint

# we name the blueprint dashboard
# the template folder is called templates. File names passed to render_template are relative to this path
dashboard = Blueprint("dashboard", __name__, template_folder="templates")


ACTIVE_ROOMS = {}


from . import dashboard_routes, dashboard_events, dashboard_api


# End file __init__.py