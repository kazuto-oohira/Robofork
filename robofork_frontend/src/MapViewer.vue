<template>
  <div id="map-viewer">
    <div id="map-container" :style="containerStyles">
      <img v-if="config" id="map-img" :src="config.imageUrl">
      <svg id="map-draw-layer">
        <circle v-for="(node, index) in mainNodes" r="8" fill="blue" :cx="mapX[index]" :cy="mapY[index]" @click="click(node)" :title="node.id"></circle>
      </svg>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

const OPERATION_ENDPOINT = '/static/robofork_app/api/operation_control.json';

export default {
  name: 'map-viewer',

  data() {
    return {
      mainNodes: [],
      config: {},
    }
  },

  computed: {
    containerStyles: function() {
      return {
        width: `${this.config.imageWidth}px`,
        height: `${this.config.imageHeight}px`,
      };
    },
    unitX: function() {
      return this.config.imageWidth / Number(this.config.scaleX);
    },
    unitY: function() {
      return this.config.imageHeight / Number(this.config.scaleY);
    },
    mapX: function() {
      return this.mainNodes.map((item) => {
        const offsetX = Number(item.x) + Number(this.config.offsetX);
        return offsetX * this.unitX + this.config.imageWidth;
      });
    },
    mapY: function() {
      return this.mainNodes.map((item) => {
        const offsetY = Number(item.y) + Number(this.config.offsetY);
        return -offsetY * this.unitY;
      });
    },
  },

  created() {
    axios.get(OPERATION_ENDPOINT)
      .then((resp) => {
        if ('config' in resp.data) {
          this.config = resp.data.config;
        }
        if ('mainNodes' in resp.data) {
          this.mainNodes = resp.data.mainNodes;
        }
      });
  },

  methods: {
    click: function(node) {
      alert(`node.id is ${node.id}`);
    },

    reset: function() {
      this.mainCommands.reset();
    },
  },
}
</script>

<style>
#map-container {
  position: relative;
  select: none;
}
#map-img {
  width: 100%;
  height: 100%;
  position: relative;
}
#map-draw-layer {
  width: 100%;
  height: 100%;
  position: absolute;
  left: 0;
  top: 0;
}
#map-draw-layer circle {
 cursor: pointer;
}
</style>
