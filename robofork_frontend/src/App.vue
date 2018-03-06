<template>
  <div class="container operation-plan-detail">
    <div class="row">
      <div class="col-xs-6">
        <h2>マップ画面</h2>
        <map-viewer
          :config="config"
          :parentRoutes.sync="routes"
          :loaded="loaded"
        ></map-viewer>
      </div>
      <div class="col-xs-6">
        <h2>指示画面</h2>
        <command-viewer
          :routes="routes"
        ></command-viewer>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

import MapViewer from './MapViewer.vue'
import CommandViewer from './CommandViewer.vue'

const OPERATION_ENDPOINT = '/static/robofork_app/api/operation_control.json';

export default {
  name: 'app',
  render: h => h(this),

  components: {
    'map-viewer': MapViewer,
    'command-viewer': CommandViewer,
  },

  data () {
    return {
      loaded: false,
      config: {},
      routes: [],
    }
  },

  created() {
    axios.get(OPERATION_ENDPOINT)
      .then((resp) => {
        if ('config' in resp.data) {
          this.config = resp.data.config;
        }

        // lazy load はめんどそうなので loaded でチェック
        this.loaded = true;
      });
  },
}
</script>
