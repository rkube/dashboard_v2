<template>
  <div>
    <input v-model="coll_name" placeholder="ABCDEF"/>
    <button v-on:click="query_collection">Query collection</button>
    <p>Collection name is {{ coll_name }}</p>
  </div>
</template>

<script>
const axios = require("axios").default;

export default {
  name: "CollSelector",
  data: function() {
    return {
      coll_name: "4HWUVK",
      run_config: ""
    };
  },
  methods: {
    query_collection: function() {
      var vm = this;
      var request = "/dashboard/query_db?coll_name=" + vm.coll_name;
      axios.get(request).then(function (response) {
        console.log(response.data);
        vm.$store.dispatch("set_run_config", response.data);
        console.log("Back in query_collection: " + vm.$store.state.run_config.run_id);
      });      
    }
  }
};
</script>
