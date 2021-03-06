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
import Vue from 'vue'
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

      const loadConfigPromise = axios.get(Constants.CONFIG_ENDPOINT(this.locationId));
      const loadVehiclesPromise = axios.get(Constants.VEHICLES_ENDPOINT(this.locationId));

      loadConfigPromise
        .then(response => {
          const config = response.data;

          if ('config' in config) {
            this.config = config.config;
          } else {
            throw new Error('not exist config');
          }

          return loadVehiclesPromise;
        })
        .then(response => {
          const vehicles = response.data;

          if (!('vehicles' in vehicles) || vehicles.vehicles.length <= 0) {
            throw new Error('not exist vehicles');
          }

          this.vehicles = vehicles.vehicles;

          this.connectWebsocket();
        })
        .catch(error => {
          console.error(error);

          return;
        });
    },

    update(index) {
      const loadVehiclesPromise = axios.get(Constants.VEHICLES_ENDPOINT(this.locationId));

      loadVehiclesPromise
        .then(response => {
          const vehicles = response.data;

          if (!('vehicles' in vehicles) || vehicles.vehicles.length <= 0) {
            throw new Error('not exist vehicles');
          }

          Vue.set(this.vehicles, index, vehicles.vehicles[index]);
        })
        .catch(error => {
          console.error(error);

          return;
        });
    },

    connectWebsocket() {
      const url = Constants.VEHICLES_UPDATE_ENDPOINT(window.location.host, this.locationId);
      const client = new W3CWebSocket(url);
      this.reconnectInterval = 1;

      client.onerror = (error) => {
        console.error('error', error);
      };

      client.onclose = () => {
        this.reconnectInterval *= 2;
        setTimeout(() => { this.connectWebsocket() }, this.reconnectInterval);
      };

      client.onmessage = (event) => {
        if (!('data' in event)) {
          return;
        }

        const parsedData = JSON.parse(event.data);
        // console.log(parsedData);

        if ('vehicles' in parsedData) {
          parsedData.vehicles.forEach((item, index) => {
            if (('reload' in item) && item.reload) {
              this.update(index);
            }
          });

          this.updateVehicles = parsedData.vehicles;
        }
      };
    },
  },
}
</script>
