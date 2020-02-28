Live visualization for data pushed to a mongodb database

The current layout in all its un-css'ed glory: 
(https://github.com/rkube/dashboard_v2/blob/master/doc/dashboard_v2.png)

Renders a live-plot of data pushed to a mongodb database to a web-page.

* The render component is implemented using vue.js and plotly
* The backend is written in flask and uses mongodb




## Used resources for this dashboard
We are using flask with blueprints to show the user a html file with different vue components



The structure of the project folder is copied from
[https://github.com/miguelgrinberg/Flask-SocketIO-Chat][https://github.com/miguelgrinberg/Flask-SocketIO-Chat]

Run the app from within the dashboard_v2 folder like this:
$ python backend.py

Notes:
Start with --no-reload when using socketio:
[https://github.com/miguelgrinberg/Flask-SocketIO/issues/508][https://github.com/miguelgrinberg/Flask-SocketIO/issues/508]

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


