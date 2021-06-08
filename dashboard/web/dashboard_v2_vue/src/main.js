import Vue from "vue";
import App from "./App.vue";
import store from "./store.js";
import Loading from "vue-loading-overlay";
import "vue-loading-overlay/dist/vue-loading.css";

Vue.component("loading-overlay", Loading);

Vue.config.productionTip = false;

new Vue({
  store: store,
  created: function() {
    console.log(
      "App is created. location: " + location.host + ", port:" + location.port
    );
  },
  render: h => h(App)
}).$mount("#app");
