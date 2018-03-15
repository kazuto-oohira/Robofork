<template>
  <map-multi-viewer
    :width="config.imageWidth"
    :height="config.imageHeight"
    :scaleX="Number(config.scaleX)"
    :scaleY="Number(config.scaleY)"
    :offsetX="Number(config.offsetX)"
    :offsetY="Number(config.offsetY)"
    :imageUrl="config.imageUrl"
    :vehicles="vehicles"
    :updateVehicles="updateVehicles"
  ></map-multi-viewer>
</template>

<script>
import axios from 'axios'
import { w3cwebsocket as W3CWebSocket } from 'websocket'

import * as Constants from './Constants'
import MapMultiViewer from './MapMultiViewer'

export default {
  name: 'home',

  components: {
    'map-multi-viewer': MapMultiViewer,
  },

  data () {
    return {
      config: {},
      vehicles: [],
      updateVehicles: [],
      locationId: this.$route.params.locationId,
    }
  },

  created() {
    this.initialize();
  },

  methods: {
    initialize() {
      this.config = {};
      this.vehicles = [];
      this.updateVehicles = [];

      // dummy json
      const loadVehiclesPromise = axios.get('/static/robofork_app/api/positions.json');
      // const loadVehiclesPromise = axios.get(Constants.VEHICLES_ENDPOINT);

      loadVehiclesPromise
        .then(response => {
          const vehicles = response.data;

          if (!('vehicles' in vehicles) || vehicles.vehicles.length <= 0) {
            throw new Error('not exist vehicles');
          }

          this.vehicles = vehicles.vehicles;

          // 運行計画は複数存在するが、マップ情報はどれも共通のため、
          // 1つ目の operation_plan_id を拾って API を叩き、マップ情報を得る
          const anyOperationPlanId = vehicles.vehicles[0].vehicle_status.vehicle_operation_plan_id;

          return axios.get(Constants.CONFIG_ENDPOINT(anyOperationPlanId));
        })
        .then(response => {
          const config = response.data;

          if ('config' in config) {
            this.config = config.config;
          } else {
            throw new Error('not exist config');
          }

          this.connectWebsocket();
        })
        .catch(error => {
          console.error(error);

          return;
        });
    },

    connectWebsocket() {
      const client = new W3CWebSocket(Constants.VEHICLES_UPDATE_ENDPOINT);
      this.reconnectInterval = 1;

      client.onerror = (error) => {
        console.error('error', error);
      };

      client.onopen = () => {
        console.log('opened');
      };

      client.onclose = () => {
        console.log('closed');

        this.reconnectInterval *= 2;
        this.connectWebsocket();
      };

      client.onmessage = (event) => {
        if (!('data' in event)) {
          return;
        }

        const parsedData = JSON.parse(event.data);
        console.log(parsedData);

        if (('reload' in parsedData) && parsedData.reload) {
          this.initialize();
          return;
        }

        if ('vehicles' in parsedData) {
          this.updateVehicles = parsedData.vehicles;
        }
      };
    },
  },
}
</script>