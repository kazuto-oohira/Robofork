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
      config: {},
      vehicles: [],
      locationId: this.$route.params.locationId,
    }
  },

  created() {
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
      })
      .catch(error => {
        console.error(error);

        return;
      });
  },
}
</script>
