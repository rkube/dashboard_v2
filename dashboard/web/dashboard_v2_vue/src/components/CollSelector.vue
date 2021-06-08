<template>
  <div>
    <input v-model="coll_name" placeholder="ABCDEF" />
    <!--button v-on:click="query_collection">Query collection</button-->
    <loading-overlay :active.sync="isLoading" :is-full-page="fullPage" :loader="icon">
      <div class="loader__container"></div>
    </loading-overlay >
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
      console.log("starting query_location");
      this.isLoading = true;
      setTimeout(() => {
        this.isLoading = false
      }, 5000);
      /*var vm = this;
      var request = "/dashboard/query_db?coll_name=" + vm.coll_name;
      axios.get(request).then(function(response) {
        console.log(response.data);
        vm.$store.dispatch("set_run_config", response.data);
        console.log(
          "Back in query_collection: " + vm.$store.state.run_config.run_id
        );
      });
      //this.isLoading = false;*/
      console.log("ended query_location");
    }
  }
};
</script>
