<template>
  <div id="app">
    <div class="container">
      <div class="row">
        <CollSelector/>
      </div>
      <div class="row">
        <DashboardView plotid="plot1"></DashboardView>
      </div>
      <div class="row">
        <DashboardView plotid="plot2"></DashboardView>
      </div>
    </div>
  </div>
</template>

<script>
import Vue from "vue/dist/vue.js";
import CollSelector from "./components/CollSelector.vue";
import DashboardView from "./components/DashboardView.vue";


Vue.config.productionTip = false;
export default {
  components: {
    CollSelector,
    DashboardView
  }
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>
