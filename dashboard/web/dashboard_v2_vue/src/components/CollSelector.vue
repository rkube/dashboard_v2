<template>
  <div>
    <input v-model="coll_name" placeholder="ABCDEF" />
    <!--button v-on:click="query_collection">Query collection</button-->
    <loading :active="isLoading" :is-full-page="fullPage" :loader="icon" />
    <button @click.prevent="query_collection">Query collection</button>
    <p>Collection name is {{ coll_name }}</p>
  </div>
</template>

<script>
import Loading from "vue-loading-overlay";
import "vue-loading-overlay/dist/vue-loading.css";
const axios = require("axios").default;

export default {
  name: "CollSelector",
  data() {
    return {
      coll_name: "ABC123",
      run_config: "",
      isLoading: false,
      fullPage: false,
      icon: "dots"
    };
  },
  components: {
    Loading
  },
  methods: {
    query_collection: function() {
      var vm = this;
      console.log("starting query_collection()");
      this.isLoading = true;
      setTimeout(() => {
        this.isLoading = false
      }, 5000);
      var url = "/dashboard/query_db?coll_name=" + vm.coll_name;
      console.log(url);
      // Await a request
      // We do all assignment in the then since fetch returns a promise.
      // See: https://dev.to/ramonak/javascript-how-to-access-the-return-value-of-a-promise-object-1bck
      fetch(url).then( function(response) {
                console.log("Fetching shot configuration: " + response.ok); // This logs true if we got a good respnse
                return(response.json())  // This returns the json of the response to the next >>then<< functions
        });
      
      console.log("this.$store.some_value" + this.$store.some_value);
      this.$store.commit("set_run_config", {"item": 123});

      //axios.get(request).then(function(response) {
      //  console.log(response.data);
      //  vm.$store.dispatch("set_run_config", response.data);
      //  console.log(
      //    "Back in query_collection: " + vm.$store.state.run_config.run_id
      //  );
      //});
      //this.isLoading = false;*/
      console.log("ended query_location");
    }
  }
};
</script>
