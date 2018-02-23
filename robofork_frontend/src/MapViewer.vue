<template>
  <div id="map-viewer">
    <p>MapViewer component here</p>
    <div id="map-container">
      <img id="map-img" :src="mapImage">
      <svg id="map-draw-layer">
        <circle v-for="node in nodes" r="8" fill="blue" :cx="node.x" :cy="node.y" @click="click(node)"></circle>
      </svg>
    </div>
  </div>
</template>

<script>
export default {
  name: 'map-viewer',
  data () {
    return {
      nodes: [
        { id: 1, x:69,  y:104, neighbors: [2]    },
        { id: 2, x:69,  y:198, neighbors: [1, 3] },
        { id: 3, x:194, y:245, neighbors: [2, 4] },
        { id: 4, x:231, y:198, neighbors: [3, 5] },
        { id: 5, x:231, y:104, neighbors: [4]    },
      ],
      mapImage: '/static/robofork_app/img/test/map1.jpg',
    }
  },
  methods: {
    click: function(node) {
      window.alert(`${node.x} / ${node.y}`);
    },
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
