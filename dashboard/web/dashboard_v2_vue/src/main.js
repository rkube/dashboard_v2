// import Loading from "vue-loading-overlay";
// import "vue-loading-overlay/dist/vue-loading.css";

import { createApp } from 'vue'
import { createStore } from 'vuex'
import axios from 'axios'
import App from './App.vue'

// Consume REST API in this store to get f.ex. the shot config.
const store = createStore({
  state () {
    return {
      collections_name: null,
      run_config: null,
      count: 123
    }
  },
  actions: {
    // TODO: how do I pass arguments here?
    // https://github.com/lukehoban/es6features#destructuring
    // The {} parenthesis pick one item from a json object and pass only this.
    // The reason we query the run config in an action is that actions can be async. Mutations can not be async.
    query_run_config({ commit }, url) {
      // query_run_config will load the response from that url as the run_config
      axios.get(url).then(function (response) {
        // Call the mutation with the response data
        commit('set_run_config', response.data);
      })
    }
  },
  mutations: {
    set_run_config(state, run_config) {
      console.log("mutation set_run_config: ")
      console.log(run_config);
      state.run_config = run_config;
      state.collection_name = run_config.run_id;
    },
    increment (state) {
      state.count++
    }
  },
  getters: {
    get_run_config: state => {
      return(state.run_config);
    }
  }
});

store.commit('increment');
console.log(store.state.count);

const app = createApp(App);
app.use(store);
app.mount('#app');

