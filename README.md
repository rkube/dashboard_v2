Live web-based visualization for [delta](https://github.com/rkube/delta).
The dashboard currently provides real-time visualization of ECEi data.

See the dashboard in [action](https://www.youtube.com/watch?v=56d93cN9oNo)

The current layout in all its un-css'ed glory: 
![alt-text](https://github.com/rkube/dashboard_v2/blob/master/doc/dashboard_v2.png)


* The backend is written in python using [flask](https://flask.palletsprojects.com/en/1.1.x/)
* The frontend is written in JavaScript using [vue.js](https://vuejs.org)

The front-end of the dashboard is implemented as a single-page application. Running the dashboard
is a two-step process. First the front-end needs to be built:

```
$ cd dashboard/web/dashboard_v2_vue
$ npm install
$ ./node_modules/.bin/vue-cli-service build
```

Then the backend can be started from the main directory
```
$ python backend.py 
```

Finally, the dashboard is accessible at http://localhost:5000/dashboard/newvue.





