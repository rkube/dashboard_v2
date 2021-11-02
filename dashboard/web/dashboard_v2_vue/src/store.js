import Vuex from "vuex";
import Vue from "vue";

Vue.use(Vuex);

//const dashboard_store = new Vuex.Store({
export default new Vuex.Store({
  state: {
    collection_name: null,
    run_config: null
  },
  mutations: {
    // update the state from here
    set_run_config(state, run_config) {
      console.log("set_run_config: " + run_config);
      state.run_config = run_config;
      state.collection_name = run_config.run_id;
    }
  },
  actions: {
    // call mutations in here
    set_run_config(context, new_run_config) {
      context.commit("set_run_config", new_run_config);
    }
  },
  getters: {
    get_run_config: state => {
      return( state.run_config);
    }
  }
});
