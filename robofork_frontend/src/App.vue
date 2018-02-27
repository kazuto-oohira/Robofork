<template>
  <div class="container operation-plan-detail">
    <div class="row">
      <div class="col-xs-6">
        <h2>マップ画面</h2>
        <map-viewer
          :config="config"
          :mainNodes="mainNodes"
          :subNodes="subNodes"
          :history="history"
          :parentRoutes.sync="routes"
          :loaded="loaded"
          ></map-viewer>
      </div>
      <div class="col-xs-6">
        <h2>指示画面</h2>
        <command-viewer
          :mainNodes="mainNodes"
          :routes="routes"
        ></command-viewer>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import undo from 'undo-manager'

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
      mainNodes: [],
      subNodes: [],
      config: {},
      routes: [],
      history: null,
    }
  },

  created() {
    this.history = new undo();

    axios.get(OPERATION_ENDPOINT)
      .then((resp) => {
        if ('config' in resp.data) {
          this.config = resp.data.config;
        }
        if ('mainNodes' in resp.data) {
          this.mainNodes = resp.data.mainNodes;
        }
        if ('subNodes' in resp.data) {
          this.subNodes = resp.data.subNodes;
        }

        // lazy load はめんどそうなので loaded でチェック
        this.loaded = true;
      });
  },
}
</script>
