<template>
  <div>
    <label> Group</label>
    <select v-model="selected_grp">
      <option v-for="group in groups" v-bind:value="group">
        {{ group }}
      </option>
    </select>
    <br /> 

    <label> Ch1_h </label>
    <select v-model="selected_ch1_h">
    <option v-for="ch1_h in h_channels" v-bind:value="ch1_h">
        {{ ch1_h | zero_pad }}
    </option>
    </select>
    <label> Ch1_v </label>
    <select v-model="selected_ch1_v">
    <option v-for="ch1_v in v_channels" v-bind:value="ch1_v">
        {{ ch1_v | zero_pad}}
    </option>
    </select>

    <br>
    <label> Ch2_h </label>
    <select v-model="selected_ch2_h">
    <option v-for="ch2_h in h_channels" v-bind:value="ch2_h">
        {{ ch2_h | zero_pad}}
    </option>
    </select>
    <label> Ch2_v </label>
    <select v-model="selected_ch2_v">
    <option v-for="ch2_v in v_channels" v-bind:value="ch2_v">
        {{ ch2_v | zero_pad}}
    </option>
    </select>

    <br>
    <label>Analysis</label>
    <select v-model="selected_anl">
    <option v-for="anl in analysis" v-bind:value="anl">
        {{anl}}
    </option>
    </select>

    <br>
    <button v-on:click="onClicked_comp">Join room</button>
    <p>I'm now in room {{ current_room }}.</p>

    <div :id="plotid" style="width:600px;height:250px;"></div>
</div>
</template>

<script>
import Plotly from "plotly.js-dist/plotly";
import io from "socket.io-client";
const axios = require("axios").default;

export default {
  name: "DashboardView",
  props: ["plotid"],
  template: `<div>
               <h1> Hello  "{{ plotid }}" </h1>
               <div :ref="plotid" :id="plotid"></div>
               <button v-on:click="button_click_func">You clicked me {{ count }} times.</button>
              </div>`,
  data: function() {
    return {
      counter: 0,
      message: "",
      current_room: null,
      selected_grp: "L",
      selected_ch1_h: 1,
      selected_ch1_v: 1,
      selected_ch2_h: 1,
      selected_ch2_v: 1,
      selected_anl: "cross_correlation",
      groups: ["G", "H", "L"],
      // The syntax for the array produces something akin to range(1,24)
      h_channels: [...Array(24).keys()].map(x => x + 1),
      v_channels: [...Array(8).keys()].map(x => x + 1),
      analysis: ["cross_correlation", "coherence", "cross_phase", "cross_power"],
      foo: 0,
      socket: io.connect("http://" + document.domain + ":" + location.port),
      current_data: null,
      traces: [
        {
          x: [10.0, 20.0, 30.0, 40.0, 50.0],
          y: [1.0, 2.0],
          z: [[-1.0, -1.0, -1.1, -1.0, -1.0], [-1.0, -1.0, -1.1, -1.0, -1.0]],
          type: "contour"
        }]
    };
  },
  methods: {
    button_click_func: function()
    {
      console.log("Clicked the button: " + this.count, " y[0] = ", this.data[0].y[0]);
      this.count += 1;
      this.$set(this.data[0].y, 0, this.data[0].y[0] + 1);
    },
    onClicked_comp: async function()
    {
      // We need to make a reference to this if we want to access the
      // member variables of data in this method:
      // https://stackoverflow.com/questions/36176073/what-is-vue-way-to-access-to-data-from-methods
      var vm = this;
      this.counter += 1;
      console.log("I am onClicked_comp. selected_grp = " + this.selected_grp
                   + ", ch1_h = " + this.selected_ch1_h
                   + ", ch1_v = " + this.selected_ch1_v
                   + ", ch1_h = " + this.selected_ch2_h
                   + ", ch2_v = " + this.selected_ch2_v
                   + ", analysis = " + this.selected_anl)  
      await axios.get("/dashboard/subscribed_rooms", { params: { sid: vm.socket.id } })
        .then(function(response) {
          response.data.subscribed_rooms.forEach(function(entry) {
            vm.socket.emit("request-leave", { sid: vm.socket.id, room: entry });
            vm.current_room = "Empty";
          });
      });
      await axios.get("/dashboard/open_rooms",
        {
          params: {
            ch_grp: this.selected_grp,
            analysis: this.selected_anl,
            sid: this.socket.id,
            ch1_h: this.selected_ch1_h,
            ch1_v: this.selected_ch1_v,
            ch2_h: this.selected_ch2_h,
            ch2_v: this.selected_ch2_v
          }
        })
        .then(function(response) {
          vm.socket.emit("request-join", {
            sid: vm.socket.id, room: response.data.active_room
          });
          vm.current_room = response.data.active_room;
        });
    }
  },
  created() {
    var vm = this;
    console.log("Component created. websocket id = " + vm.socket.id);
    // Install socket.emit hook. This routine receives the updated data packet from
    // the backend and prepares it for the plotly plot.
    var j = 0;
    var t = 0;
    var k = 0;
    var update = null;

    vm.socket.on("new_data", function (msg) {
      vm.current_data = msg["data"];
      console.log("I just got new data" + msg["data"].length);
      //console.log("Length of current x-axis: " + vm.traces[0].x.length)
      //console.log("This is the current x-axis: " + vm.traces[0].x);

      // If-clause will likely be executed when the first data packet arrives.
      // Create new x-axis.
      if (msg["data"].length != vm.traces[0].x.length) {
        console.log("Received data with more data than current x-axis!");
        // x-axis is frequency
        var new_x = [...Array(msg["data"].length).keys()];
        // y-axis is time
        var new_y = new Array(10);
        // z-data is amplitude at a given frequency and time
        var new_z = new Array(10);
        
        // Create new y-values.
        // Create new 2d-array structure for z
        for(j = 0; j < 10; j++)
        {
          new_y[j] = j;
          new_z[j] = new Array(msg["data"].length);
        }
          
        // Initialize new_z with zeros, except the first row.
        for (t = 1; t < 10; t++)
        {
          for(j = 0; j < new_x.length; j++)
          {
            new_z[t][j] = 0.0;
          }
        }
        // After initialization, put the new data into new_z[0][..]
        for(j = 0; j < new_x.length; j++)
        {
          new_z[0][j] = msg["data"][j];
        }
        
        console.log("Updating: new_x = " + new_x);
        console.log("Updating: new_y = " + new_y);
        console.log("Updating: new_z = " + new_z);
        // Generate the plot-update
        update = {x: [new_x], y: [new_y], z: [new_z]};
        console.log("Updating plot at plotdiv" + vm.$props.plotid);
        Plotly.restyle(vm.$props.plotid, update);
      }
      // Here we already have the y-axis and the z-array.
      // We only need to push-back the data in the z-array by one as to make space for the
      // new data. We also need to insert the new data.
      else {
        console.log("New data as same length as current x-axis");
        //var cur_y = vm.traces[0].y;
        var cur_z = vm.traces[0].z;
        // Push data in z back by one row.
        for (t = 0; t < 10 - 1; t++) {
          for (k = 0; k < cur_z[0].length; k++) {
            cur_z[t][k] = cur_z[t + 1][k];
          }
        }
        for (k = 0; k < cur_z[10 - 1].length; k++) {
          cur_z[10 - 1][k] = msg["data"][k];
        }
        update = { z: [cur_z] };
        console.log("Updating plot at plotdiv" + vm.$props.plotid);
        Plotly.restyle(vm.$props.plotid, update);
      }
    });
  },
  mounted: function() {
    var vm = this;
    console.log("I am mounted. My plotid is " + vm.$props.plotid);
    Plotly.react(vm.$props.plotid, vm.traces);
  },
  filters: {
    zero_pad: function(value) {
      if (value < 10) return "0" + value;
      else return "" + value;
    }
  }
};
</script>
