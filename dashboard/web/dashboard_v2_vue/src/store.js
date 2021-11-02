// This has moved to main.js
// import { createStore} from 'vuex'
// export default createStore({
//     state() {
//       return {
//         collections_name: null,
//         run_config: null
//       }
//     },
//     mutations: {
//       set_run_config(state, run_config) {
//         console.log("mutation set_run_config: " + run_config);
//         state.run_config = run_config;
//         state.collection_name = run_config.run_id;
//       }
//     },
//     getters: {
//       get_run_config: state => {
//         return(state.run_config);
//       }
//     }
//   });