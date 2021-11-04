<template>
  <div>
    <input v-model="coll_name" placeholder="ABCDEF" />
    <!--button v-on:click="query_collection">Query collection</button-->
    <loading :active="isLoading" :is-full-page="fullPage" :loader="icon" />
    <button @click.prevent="query_collection">Query collection</button>
    <p>Loaded collection {{ coll_name }}</p>
  </div>
</template>

<script>
import Loading from "vue-loading-overlay";
import "vue-loading-overlay/dist/vue-loading.css";

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
    query_collection: async function() {
      var vm = this;
      console.log("starting query_collection()");
      this.isLoading = true;
      setTimeout(() => {
        this.isLoading = false
      }, 5000);
      var url = "/dashboard/query_db?coll_name=" + vm.coll_name;
      // query_run_config will load the response from that url as the run_config
      this.$store.dispatch("query_run_config", url);
      this.isLoading = false;
    }
  }
};
</script>
