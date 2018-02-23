import Vue from 'vue'
import MapViewer from './MapViewer.vue'
import CommandViewer from './CommandViewer.vue'

new Vue({
  el: '#app',
  components: {
    'map-viewer': MapViewer,
    'command-viewer': CommandViewer,
  },
})
