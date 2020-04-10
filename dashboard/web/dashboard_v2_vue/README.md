# dashboard_v2_vue
These are the vue.js dependent components of the backend. The required npm packages are
* @vue/cli-service@4.3.1
* axios@0.19.2
* plotly.js-dist@1.53.0
* socket.io@2.3.0
* vue@2.6.11
* vue-router@3.1.6
* vuex@3.1.3


### Compiles and minifies for production
Ensure that vue-cli-service builds the templates in the template directory
of the parent flask app. Per default, outputDir in vue.config.js should be '../../templates'.
```
./node_modules/bin/vue-cli-service build --mode development --no-clean
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).
