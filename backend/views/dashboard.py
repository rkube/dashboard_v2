# -*- Encoding: UTF-8 -*-
# file dashboard_v2/backend/views/dashboard.py

from flask import Blueprint, render_template

dashboard = Blueprint("dashboard", __name__)

@dashboard.route('/hello')
def hello_dashboard():
    print("hello_dashboard")
    return render_template("templates/hello_dashboard.html")

# End of file dashboard.py