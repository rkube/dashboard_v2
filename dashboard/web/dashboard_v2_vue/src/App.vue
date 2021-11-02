<template>
<body>
  <h1> DELTA ECEi dashboard</h1>
  <div id="my-app">
    <div class="container">
      <div class="row">
         <CollSelector/>
      </div>
      <!--div class="row">
         <ECEIPlayer/>
      </div-->
      <!--div class="row">
        <DashboardView plotid="plot1"></DashboardView>
      </div-->
      <!--div class="row">
        <DashboardView plotid="plot2"></DashboardView>
      </div-->
    </div>
  </div>
  </body>
</template>


// Script section:
// Javascript imports, data handling, etc.
<script>

import CollSelector from "./components/CollSelector.vue";
// import DashboardView from "./components/DashboardView.vue";
// import ECEIPlayer from "./components/ECEIPlayer.vue";


export default {
  name: 'ECEIdashboard',
  components: {
    CollSelector
    // ECEIPlayer,
    // DashboardView
  }
}
</script>

// Style section
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
