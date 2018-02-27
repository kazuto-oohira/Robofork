<template>
  <div class="container operation-plan-detail">
    <div class="row">
      <div class="col-xs-6">
        <h2>マップ画面</h2>
        <map-viewer></map-viewer>
      </div>
      <div class="col-xs-6">
        <h2>指示画面</h2>
        <command-viewer></command-viewer>
      </div>
    </div>
  </div>
</template>

<script>
import MapViewer from './MapViewer.vue'
import CommandViewer from './CommandViewer.vue'

export default {
  name: 'app',
  render: h => h(this),

  components: {
    'map-viewer': MapViewer,
    'command-viewer': CommandViewer,
  },

  data () {
    return {
    }
  },
}
</script>
