# File dashboard/main/__init__.py
# -*- Encoding: UTF-8 -*-

from flask import Blueprint
dashboard = Blueprint("dashboard", __name__, template_folder="templates")

ACTIVE_ROOMS = {}

from . import dashboard_api, dashboard_events, dashboard_routes
from .datasets import ECEIDataset
from .models import UNet

 # End of file dashboard/main/__init__.py