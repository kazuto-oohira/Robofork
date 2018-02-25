<template>
  <div id="map-viewer">
    <div id="map-container">
      <img v-if="mapImage" id="map-img" :src="mapImage.url" :width="mapImage.width" :height="mapImage.height">
      <svg id="map-draw-layer">
        <circle v-for="node in nodes" r="8" fill="blue" :cx="node.x" :cy="node.y" @click="click(node)"></circle>
      </svg>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

const OPERATION_ENDPOINT = '/static/robofork_app/api/operation_control.json';

export default {
  name: 'map-viewer',
  data () {
    return {
      nodes: [],
      mapImage: {},
    }
  },

  methods: {
    click: function(node) {
      window.alert(`${node.x} / ${node.y}`);
    },
  },

  created() {
    axios.get(OPERATION_ENDPOINT)
      .then((resp) => {
        if ('nodes' in resp.data) {
          this.nodes = resp.data.nodes;
        }
        if ('mapImage' in resp.data) {
          this.mapImage = resp.data.mapImage;
        }
      });
  },
}
</script>

<style>
#map-container {
  position: relative;
  width: 460px;
  height: 580px;
}
#map-img {
  position: relative;
  width: 460px;
  height: 580px;
}
#map-draw-layer {
  position: absolute;
  width: 460px;
  height: 580px;
  top: 0;
  left: 0;
}
#map-draw-layer circle {
 cursor: pointer;
}
</style>
