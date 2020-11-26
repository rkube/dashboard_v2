<template>
  <div>
    <div class="column">
      <label>Select a time chunk</label>
      <select v-model="selected_time_chunk">
        <option v-for="chunk in available_time_chunks" v-bind:key="chunk">
          {{ chunk }}
        </option>
      </select>
    </div>
    <div class="column">
      <button v-on:click="refresh_time_chunks">Refresh</button>
    </div>
    <div class="row">
      <button v-on:click="get_time_chunk_data">Load data</button>
    </div>
    <div class="column">
      <div>Time index in chunk {{selected_time_idx}}</div>
      <vue-slider 
        v-model="selected_time_idx"
        v-on:change="update_plot_tidx"
        :min="0"
        :max="9999"
        :interval="1"
        :lazy="true"
      ></vue-slider>
    </div>
    <div class="row" style="background-color=#22a;">
      <div id="ecei_plot" ref="ecei_plot"></div>
    </div>
  </div>
</template>

<script>
import Plotly from "plotly.js-dist/plotly";
const axios = require("axios").default;
// Load entire mathjs library, see here:https://mathjs.org/docs/custom_bundling.html
import { create, all } from 'mathjs'
const math = create(all);
import VueSlider from 'vue-slider-component';
import 'vue-slider-component/theme/default.css'


export default {
  name: "ECEIPlayer",
  components: {
    VueSlider
  },
  data: function() {
    return {
      selected_time_chunk: 0,
      current_time_chunk: 0,
      available_time_chunks: [0],
      time_chunk_data: null,
      selected_time_idx: 50,
      traces: [
        {
          x: [1, 2, 3, 4, 5, 6, 7, 8],
          y: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24],
          type: "contour"
        }
      ]
    };
  },
  methods: {
    refresh_time_chunks: async function() {
      // Query available ECEI time chunks for the selected collection
      // Access the current collection name. We do this by quering the vuex store.
      // See https://www.smashingmagazine.com/2020/01/data-components-vue-js/
      // Async function needed so that we can use await axios.get call.
      var run_id = this.$store.getters.get_run_config.run_id;
      console.log("Refreshing time chunks. Collection is: " + run_id);

      var request = "/dashboard/available_ecei_frames?run_id=" + run_id;
      // let is block scope. Inside a function this is the same as a variable
      // See: https://www.w3schools.com/JS/js_let.asp
      let response = await axios.get(request);
      console.log("refresh_time_chunks: response");
      console.log(response);
      this.available_time_chunks = response.data["available_chunks"];

      if(this.available_time_chunks.includes(this.selected_time_chunk) == false) {
        this.selected_time_chunk = this.available_time_chunks[0];
      }
    },
    get_time_chunk_data: async function() {
      var run_id = this.$store.getters.get_run_config.run_id;
      // Cache data from selected time chunk locally for plotting.
      if(this.selected_time_chunk !== this.current_time_chunk)
      {
        console.log("Fetching time chunk data");
        var request = "/dashboard/get_ecei_frames?run_id=" + run_id + "&time_chunk_idx=" + this.selected_time_chunk
        let response = await axios.get(request);
        this.curent_time_chunk = this.selected_time_chunk;

        // Convert time_chunk_data from base64 to float64 array
        let binary_string = atob(response.data["time_chunk_data"]);
        let buffer = new ArrayBuffer(binary_string.length);
        let bytes_buffer = new Uint8Array(buffer);

        for (let i = 0; i < binary_string.length; i++) {
          bytes_buffer[i] = binary_string.charCodeAt(i);
        }

        let values = new Float64Array(buffer);
        this.time_chunk_data = Array.from(values);
        this.time_chunk_data = math.transpose(math.reshape(this.time_chunk_data, response.data["chunk_shape"]));

        this.bad_channels = response.data["bad_channels"];

        // Emulate linspace to set r and z ranges for the contour plot.
        let dr = (math.max(response.data["rarr"]) - math.min(response.data["rarr"])) / 8.0
        let r_range = math.range(math.min(response.data["rarr"]), math.max(response.data["rarr"]), dr);

        let dz = (math.max(response.data["zarr"]) - math.min(response.data["zarr"])) / 24.0
        let z_range = math.range(math.min(response.data["zarr"]), math.max(response.data["zarr"]), dz);

        let new_z = math.reshape(this.time_chunk_data[50], [8, 24]);
        // Calls to Plotly.restyle expect the data arrays wrapped in an additional array
        // https://plotly.com/javascript/plotlyjs-function-reference/#plotlyreact
        let update = {x: [r_range], y: [z_range], z: [new_z]};
        Plotly.restyle(this.$refs.ecei_plot, update);
      } // if this.selected_time_chunk != this.current_time_chunk
    },
    update_plot_tidx: function() {
      console.log("Updating the time index of the plot");
      let new_z = math.reshape(this.time_chunk_data[this.selected_time_idx], [8, 24]);
      let update = {z: [new_z]};
      Plotly.restyle(this.$refs.ecei_plot, update);
    }
  },
  mounted() {
    // var vm = this;
    console.log("ECEIPlayer mounted. collection is " + this.$store.state.run_config);
    console.log(this.$refs.ecei_plot);
    // https://stackoverflow.com/questions/36970062/vue-js-document-getelementbyid-shorthand
    let x = math.range(1, 8);
    let y = math.range(1, 24);
    let z = math.random([8, 24]);
    let data = [{z: z, x: x, y: y, type: 'contour'}];
    Plotly.newPlot(this.$refs.ecei_plot, data);
  }
};
</script>