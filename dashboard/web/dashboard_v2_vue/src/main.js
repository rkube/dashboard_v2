import Vue from "vue";
import App from "./App.vue";
import store from "./store.js";

Vue.config.productionTip = false;

new Vue({
  store,
  created: function () {
    console.log("App is created. location: " + location.host + ", port:" + location.port);
  },
  render: h => h(App)
}).$mount("#app");
