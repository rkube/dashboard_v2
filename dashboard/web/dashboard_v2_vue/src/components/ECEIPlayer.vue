<template>
  <div>
    <div class="row">
    <!--div class="column"-->
      <label>Select a time chunk</label>
      <select v-model="selected_chunk">
        <option v-for="chunk in this.$store.state.available_chunks" v-bind:key="chunk">
          {{ chunk }}
        </option>
      </select>
    <!--/div-->
    <!--div class="column"-->
      <loading :active="isLoading" :is-full-page="fullPage" :loader="icon" />
      <button v-on:click="get_time_chunk_data">Load data</button>
    <!--/div-->
    </div>
    <div class="column">
      <input 
        type="checkbox"
        v-model="show_region_proposal"
        @change="toggle_region_proposal()"
      >
      <label for="ntm-regions">Show NTM region proposal </label>
    </div>

    <div class="column">
            <div>Time index in chunk {{ selected_time_idx }}   Time in shot: {{ selected_time_str }}s</div>
      <vue-slider
        v-model="selected_time_idx"
        v-on:change="update_plot_tidx"
        :min="0"
        :max="9999"
        :interval="1"
        :lazy="true"
      ></vue-slider>
      <div
        id="ecei_plot"
        ref="ecei_plot"
        :style = "{height: '1200px', width: '600px', backgroundColor: 'powderblue'}"
      ></div>
    </div>
  </div>
</template>

<script>
import Plotly from "plotly.js-dist/plotly";
const axios = require("axios").default;
// Load entire mathjs library, see here:https://mathjs.org/docs/custom_bundling.html
import { create, all } from "mathjs";
const math = create(all);
import VueSlider from "vue-slider-component";
import "vue-slider-component/theme/default.css";
import Loading from "vue-loading-overlay";
import "vue-loading-overlay/dist/vue-loading.css";

export default {
  name: "ECEIPlayer",
  components: {
    VueSlider,
    Loading
  },
  data: function() {
    return {
      current_time_chunk: 0,
      tstart: 0.0,
      dt: 0.0001,
      show_region_proposal: false,
      time_chunk_data: null,
      time_chunk_mask: null,
      selected_time_idx: 1,
      selected_time_str: 0.0,

      traces: [
        {
          x: [1, 2, 3, 4, 5, 6, 7, 8],
          y: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24],
          type: "contour"
        }
      ],
      isLoading: false,
      fullPage: false,
      icon: "dots"
    };
  },
  computed: {
    // We want to set up a two-way data binding for the v-model in the
    // selected time chunk slider and the selected_chunk in the store.
    // To do so, I am following this tutorial blog-post: 
    // https://markus.oberlehner.net/blog/form-fields-two-way-data-binding-and-vuex/
    selected_chunk: {
      get() {
        console.log("Calling computed.selected_chunk.get");
        return this.$store.state.selected_chunk;
      },
      set(value) {
        // Check if value is in the array
        console.log("Calling computed.selected_chunk.set. New value: " + value);
        console.log(this.$store.state.available_chunks);
        this.$store.commit('set_selected_chunk', value);
      }
    }
  },
  methods: {
    get_time_chunk_data: async function() {
      // Fetches ECEI data from backend
      var run_id = this.$store.getters.get_run_config.run_id;
      // Loader
      this.isLoading = true;
      console.log("Loading data. Selected in store:  " + this.$store.state.selected_chunk);
      // Cache data from selected time chunk locally for plotting.
      if(this.current_time_chunk !== this.$store.state.selected_chunk)
      {
        // Fetch ECEI data for plotting and store returned values
        var request = "/dashboard/get_ecei_frames?run_id=" + run_id + "&time_chunk_idx=" + this.$store.state.selected_chunk;
        this.current_time_chunk = this.$store.state.selected_chunk
        let response = await axios.get(request);
        this.bad_channels = response.data["bad_channels"];
        this.tstart = response.data["tstart"];
        this.tend = response.data["tend"];
        this.dt = response.data["dt"];
        let chunk_shape = response.data["chunk_shape"];
        let meanval = response.data["meanval"];
        let stdval = response.data["stdval"];
        let binary_string = atob(response.data["time_chunk_data"]);
        let rarr = response.data["rarr"];
        let zarr = response.data["zarr"];
        
        // Convert time_chunk_data from base64 to float64 array
        let buffer = new ArrayBuffer(binary_string.length);
        let bytes_buffer = new Uint8Array(buffer);
        for (let i = 0; i < binary_string.length; i++) {
          bytes_buffer[i] = binary_string.charCodeAt(i);
        }

        let values = new Float64Array(buffer);
        this.time_chunk_data = Array.from(values);
        this.time_chunk_data = math.transpose(math.reshape(this.time_chunk_data, chunk_shape));

        // Fetch region proposal for Magnetic Island location
        request = "/dashboard/get_ecei_mask?run_id=" + run_id + "&time_chunk_idx=" + this.selected_chunk;
        response = await axios.get(request);
        binary_string = atob(response.data["all_masks"]);
        buffer = new ArrayBuffer(binary_string.length)
        bytes_buffer = new Uint8Array(buffer);
        for(let i = 0; i < binary_string.length; i++) {
          bytes_buffer[i] = binary_string.charCodeAt(i);
        };
        values = new Int8Array(buffer);
        this.time_chunk_mask = Array.from(values);
        this.time_chunk_mask = math.transpose(math.reshape(this.time_chunk_mask, chunk_shape));
        console.log("Received time_chunk_mask: ", this.time_chunk_mask);

        // For testing of the plotting code see: https://codepen.io/rkube/pen/MWjWPag

        // Emulate linspace to set r and z ranges for the contour plot.
        let dr = (math.max(rarr) - math.min(rarr)) / 7.0;
        let r_range = math.range(math.min(rarr), math.max(rarr), dr);
        console.log("r_range = ", r_range); 

        let dz = (math.max(zarr) - math.min(zarr)) / 23.0;
        let z_range = math.range(math.min(zarr), math.max(zarr), dz);
        console.log("_range = ", z_range);

        let new_z = math.reshape(this.time_chunk_data[1], [24, 8]);
        let zmin = meanval - 2.5 * stdval;
        let zmax = meanval + 2.5 * stdval;

        // Calls to Plotly.restyle expect the data arrays wrapped in an additional array
        // https://plotly.com/javascript/plotlyjs-function-reference/#plotlyreact

        let update = {
          x: [r_range._data],
          y: [z_range._data],
          z: [new_z],
          zmin: zmin,
          zmax: zmax
          };
        console.log("get_time_chunk_data. sending update to plotly", update);
        Plotly.restyle(this.$refs.ecei_plot, update);
      } // end if this.selected_time_chunk != this.current_time_chunk
      this.isLoading = false;
    },
    update_plot_tidx: function() {
      /** 
      Callback for the slider. 
      
      Updates the plot with data for the newly selected time index.
      Also updated the time in the current chunk.
      
      **/
      if(this.time_chunk_data == null){
       // Return if no data has been loaded
        return;
      }
      var new_z = math.reshape(this.time_chunk_data[this.selected_time_idx], [24, 8]);
      var data_update = {z: [new_z], ncontours: 32};
      // Set the new time in the plot title
      // Update the selected time.
      let tt = (Math.round((this.tstart + this.selected_time_idx * this.dt) * 1000000) / 1000000).toFixed(6);
      this.selected_time_str = tt; //(Math.round((this.tstart + this.selected_time_idx * this.dt) * 1000000) / 1000000).toFixed(6);
      
      Plotly.restyle(this.$refs.ecei_plot, data_update, 0);
      // Extract ECEI device name
      let dev = this.$store.state.run_config["diagnostic"]["dev"];
      Plotly.relayout(this.$refs.ecei_plot, {title: "KSTAR ECEI " + dev + " t = " + String(tt) + "s"});

      // If the magnetic island region proposal is active we need to update that plot as well
      if(this.show_region_proposal === true){
        new_z = math.reshape(this.time_chunk_mask[this.selected_time_idx], [24, 8]);
        data_update = {z: [new_z]};
        Plotly.restyle(this.$refs.ecei_plot, data_update, 1);
      }
    },
    toggle_region_proposal: function() {
      /**
       * Callback for the toggle_region_proposal checkbox.
       * 
       * Add, or remove the region proposal trace from the plot.
       */
      // selected_time_idx == 0 upon instantiation. If this is the case, make this
      // function to nothing.
      if(this.selected_time_idx === 1) {
        return;
      }

      // If we currently don't show contours for the region proposals
      // - create one
      // - add it to the plot
      if(this.show_region_proposal === true) {
        console.log("show_region_proposal was activated - adding mask contours");
        let mask_data = this.time_chunk_mask[this.selected_time_idx];
        console.log("Got mask data ", mask_data);

        var trace_mask = {
          x: this.$refs.ecei_plot.data[0].x,
          y: this.$refs.ecei_plot.data[0].y,
          z: math.reshape(this.time_chunk_mask[this.selected_time_idx], [24, 8]),
          type: 'contour',
          opacity: 0.5,
          ncontours: 6,
          zmin: -0.01,
          zmax: 4.01,
          colorscale: [
            ['0.0', 'rgb(228,26,28)'],
            ['0.2', 'rgb(55,126,184)'],
            ['0.4', 'rgb(77,175,74)'],
            ['0.6', 'rgb(152,78,163)'],
            ['0.8', 'rgb(255,127,0)'],
            ['1.0', 'rgb(255,255,1)']]
        };
        Plotly.addTraces(this.$refs.ecei_plot, trace_mask);
      } else {
        console.log("show_region_proposal was deactivated - removing mask contours");
        Plotly.deleteTraces(this.$refs.ecei_plot, -1);
      }

      // If we currntly show contours for the region proposal
      // - remove it from the plot

    console.log("toggle_region_proposal() here");
    }
  }, // end methods()
  mounted() {
    // var vm = this;
    console.log("ECEIPlayer mounted. collection is " + this.$store.state.run_config);
    // https://stackoverflow.com/questions/36970062/vue-js-document-getelementbyid-shorthand


    let x = math.range(2, 10);
    let y = math.range(1, 25);
    let z = math.random([24, 8], -0.05, 0.05);

    // We need to use the _data member of the ranges created here
    // Plotly expects x and y to be instances of array.
    // (x._data instanceof Array) evaluates true 
    // while
    // (x instanceof Array) evaluates false
    let plot_data = [{z: z, 
      x: x._data, 
      y: y._data, 
      type: 'contour', 
      ncontours: 32,
      zmin: -0.05,
      zmax: 0.05,
      colorbar: {
        title: "δTₑ/〈Tₑ〉",
        titleside: "right"
      }
      },
    ];

    let plot_layout = {
      title: "ECEI data t = -1.0s",
      xaxis: { title: "R / m" },
      yaxis: { title: "Z / m" },
      zaxis: { title: "δTₑ/〈Tₑ〉"}
    };

    let plot_config = {
      toImageButtonOptions: {
        height: 1600,
        width: 600,
        scale: 1
      }
    };
    Plotly.newPlot(this.$refs.ecei_plot, plot_data, plot_layout, plot_config);
  } // end mounted()
};
</script>
