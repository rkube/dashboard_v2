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
      // Name of the collection that is queried
      collections_name: null,
      // Run configuration used by DELTA
      run_config: null,
      // Chunks of analyzed data in the database
      available_chunks: [0],
      // Time-chunk that should currently be loaded
      selected_chunk: 0
    }
  },
  actions: {
    // TODO: how do I pass arguments here?
    // https://github.com/lukehoban/es6features#destructuring
    // The {} parenthesis pick one item from a json object and pass only this.
    // The reason we query the run config in an action is that actions can be async. Mutations can not be async.
    query_run_config({ commit, state }, url) {
      // query_run_config will load the response from that url as the run_config
      axios.get(url).then(
        function (response) {
          // Call the mutation with the response data
          commit('set_run_config', response.data);
        }
      ).then(
        function () {
          // If we successfully queried the run_config for the collection we continue by
          // fetching the available time-chunks.
          var run_config = state.run_config;
          var request = "/dashboard/available_ecei_frames?run_id=" + run_config.run_id;
          console.log("Received run_config from backend.");
          axios.get(request).then(function (response) {
            // Update the available time-chunks and set the selected chunk.
            commit('set_available_chunks', response.data["available_chunks"]);
            commit('set_selected_chunk', state.available_chunks[77]);
            console.log("Received available_chunks from backend");
          })
        }
      )
    },
    // Queries the available time chunks of the run
    query_time_chunk({ commit }) {
      var request = "/dashboard/available_ecei_frames?run_id=" + state.run_config.run_id
      axios.get(request).then(function (response) {
        commit('set_available_chunks', response.data["available_chunks"]);
      })
    }
  },
  mutations: {
    set_run_config(state, run_config) {
      state.run_config = run_config;
      state.collection_name = run_config.run_id;
    },
    set_available_chunks(state, chunks) {
      state.available_chunks = chunks;
    },
    set_selected_chunk(state, chunknr) {
      state.selected_chunk = chunknr;
    }
  },
  getters: {
    get_run_config: state => {
      return(state.run_config);
    },
    get_available_chunks : state => {
      return(state.available_chunks);
    },
    get_selected_chunk : state => {
      return(state.set_selected_chunk);
    }
  }
});


const app = createApp(App);
app.use(store);
app.mount('#app');

