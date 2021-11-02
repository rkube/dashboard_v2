// import Vue from "vue";
// import store from "./store.js";
import Loading from "vue-loading-overlay";
import "vue-loading-overlay/dist/vue-loading.css";

import { createApp } from 'vue'
import { createStore } from 'vuex'
// import store from './store'
import App from './App.vue'


const store = createStore({
  state() {
    return {
      collections_name: null,
      run_config: null,
      some_value: 123
    }
  },
  mutations: {
    set_run_config(state, run_config) {
      console.log("mutation set_run_config: " + run_config);
      state.run_config = run_config;
      state.collection_name = run_config.run_id;
    }
  },
  getters: {
    get_run_config: state => {
      return(state.run_config);
    }
  }
});

const appen = createApp(App);
appen.use(store);
appen.mount('#my-app');

