README

We are using flask with blueprints to show the user a html file with different vue components

|==============================|  
|                              |
|   |---------| |---------|    |
|   | vue     | | vue     |    |
|   | comp-   | | comp-   |    |
|   | onent   | | onent   |    |
|   |---------| |---------|    |
|                              |
|   |---------| |---------|    |
|   | vue     | | vue     |    |
|   | comp-   | | comp-   |    |
|   | onent   | | onent   |    |
|   |---------| |---------|    |
|                              |
|==============================|


The structure of the project folder is copied from
https://github.com/miguelgrinberg/Flask-SocketIO-Chat

Run the app from within the dashboard_v2 folder like this:
$ python backend.py

Notes:
Start with --no-reload when using socketio:
https://github.com/miguelgrinberg/Flask-SocketIO/issues/508
Something about flask run being overridden when socketio is loaded but not used

https://github.com/miguelgrinberg/Flask-SocketIO/issues/508#issuecomment-326782539

Resources:

FLASK blueprints:
http://exploreflask.com/en/latest/blueprints.html
https://flask.palletsprojects.com/en/1.1.x/blueprints/


Flask SocketIO+Blueprints:
https://github.com/miguelgrinberg/Flask-SocketIO-Chat/

vue integration:
https://github.com/bioudi/Flask-VueJs-SocketIO



https://www.fullstackpython.com/vuejs.html


https://madewithvuejs.com/vueplotly
https://github.com/David-Desmaisons/vue-plotly


Use a divisional layout:
http://exploreflask.com/en/latest/blueprints.html#divisional
Divisional

With the divisional structure, you organize the pieces of the application based on which
part of the app they contribute to. All of the templates, views and static files for the
admin panel go in one directory, and those for the user control panel go in another.


