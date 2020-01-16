# -*- Encoding: UTF-8 -*-
# file dashboard_v2/backend/views/dashboard.py

from flask import Blueprint, render_template, send_from_directory

# we name the blueprint dashboard
# the template folder is called templates. File names passed to render_template are relative to this path
dashboard = Blueprint("dashboard", __name__, template_folder="templates")

@dashboard.route('/hello')
def hello_dashboard():
    print("hello_dashboard")
    return render_template("hello_dashboard.html")

@dashboard.route('/hello_vue')
def hello_vue():
    print("hello_vue")
    return send_from_directory("views/templates", "hello_vue.html")
# End of file dashboard.py