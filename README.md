Live web-based visualization for [delta](https://github.com/rkube/delta)


The current layout in all its un-css'ed glory: 
![alt-text](https://github.com/rkube/dashboard_v2/blob/master/doc/dashboard_v2.png)

Renders a live-plot of data pushed to a mongodb database to a web-page.

* The render component is implemented using [vue.js](https://vuejs.org/) and [plotly](https://plot.ly/javascript/)
    * The backend is written in [flask](https://flask.palletsprojects.com/en/1.1.x/) and ingests data from [mongodb](https://www.mongodb.com/)


Run from the main directory 

```
$ export FLASK_ENV=development 
$ python backend.py 
```

Open web-browser to http://localhost:5000/dashboard/hello_vue 

