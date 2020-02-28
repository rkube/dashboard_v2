# -*- Encoding: UTF-8 -*-
# file dashboard_v2/backend/dashboard/dashboard_routes.py

from flask import render_template, send_from_directory

# we name the blueprint dashboard
# the template folder is called templates. File names passed to render_template are relative to this path
#dashboard = Blueprint("dashboard", __name__, template_folder="templates")

from . import dashboard

@dashboard.route('/hello')
def hello_dashboard():
    return render_template("hello_dashboard.html")

@dashboard.route('/hello_vue')
def hello_vue():
    return send_from_directory("templates", "hello_vue.html")
# End of file dashboard.py