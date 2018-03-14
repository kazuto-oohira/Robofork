<template>
  <map-multi-viewer
    :width="502"
    :height="394"
    :scaleX="13.210526316"
    :scaleY="10.368421053"
    :offsetX="-2.5"
    :offsetY="0"
    :imageUrl="'/static/robofork_app/img/test/map1.png'"
    :positions="positions"
  ></map-multi-viewer>
</template>

<script>
import axios from 'axios'

import * as Constants from './Constants'
import MapMultiViewer from './MapMultiViewer'

export default {
  name: 'home',

  components: {
    'map-multi-viewer': MapMultiViewer,
  },

  data () {
    return {
      vehicles: {},
      locationId: this.$route.params.locationId,
    }
  },

  computed: {
    positions() {
      if (!this.vehicles) {
        return [];
      }

      return this.vehicles.vehicle_positions;
    },
  },

  created() {
    // dummy json
    const loadVehiclesPromise = axios.get('/static/robofork_app/api/positions.json');
    // const loadVehiclesPromise = axios.get(Constants.VEHICLES_ENDPOINT);

    loadVehiclesPromise
      .then(response => {
        const vehicles = response.data;

        if ('vehicles' in vehicles) {
          this.vehicles = vehicles.vehicles[0];
        } else {
          throw new Error('not exist vehicles');
        }
      });
  },
}
</script>
