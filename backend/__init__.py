# -*- Encoding: UTF-8 -*-

"""The __init__.py serves double duty: it will contain the application factory, 
and it tells Python that the flaskr directory should be treated as a package."""

from flask import Flask

from .views.dashboard import dashboard
# Register the dashboard blueprint in the main __init__.py:



def create_app(test_config=None):
    """Creates and configures the app"""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(dashboard, url_prefix="/")

    #@app.route("/hello")
    #def hello():
    #    return("Hello, World!")
    print(app.url_map)

    return app

# End of file __init__py