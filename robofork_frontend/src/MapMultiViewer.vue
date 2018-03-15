<template>
  <div class="container-fluid" id="map-multi-viewer">
    <div class="row">
      <div class="map-container"
        :style="{ width: `${width}px`, height: `${height}px` }"
      >
        <img v-if="imageUrl" class="map-image" :src="imageUrl">
        <div class="map-draw-layer">
          <template v-for="(vehicle, index) in vehicles">
            <!-- commands -->
            <div
              v-for="command in vehicle.vehicle_positions"
              class="node"
              :style="{
                transform: `translate(${mappedX(command.x)}px, ${mappedY(command.y)}px)`
              }"
            ></div>

            <!-- roboork -->
            <div
              v-if="vehicle.vehicle_positions.length > 0"
              class="robofork"
              data-trigger="manual"
              data-toggle="popover"
              data-placement="top"
              :data-original-title="vehicleName[index]"
              :data-content="statusName[index]"
              data-animation="false"
              :data-status-code="statusCode[index]"
              :style="{
                transform: `translate(${mappedX(roboforkX[index])}px, ${mappedY(roboforkY[index])}px)`
              }"
            >
              <img
                src="/static/robofork_app/img/robofork.svg"
                alt=""
                width="30"
                height="30"
                :style="{
                  transform: `rotate(${roboforkDegree[index]}deg)`
                }"
              >
            </div>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import * as Constants from './Constants'

export default {
  name: 'map-multi-viewer',

  props: [
    'width',
    'height',
    'scaleX',
    'scaleY',
    'offsetX',
    'offsetY',
    'imageUrl',
    'vehicles',
    'updateVehicles',
  ],

  data() {
    return {
    }
  },

  computed: {
    commands() {
      if (!this.vehicles || this.vehicles.length <= 0) {
        return [];
      }

      return this.vehicles[0].vehicle_positions;
    },

    vehicleName() {
      return this.vehicles.map(vehicle => vehicle.name);
    },

    statusName() {
      return this.vehicles.map(vehicle => vehicle.vehicle_status.status_name);
    },

    statusCode() {
      return this.vehicles.map(vehicle => vehicle.vehicle_status.status_code);
    },

    unitX() {
      return this.width / this.scaleX;
    },

    unitY() {
      return this.height / this.scaleY;
    },

    latestDir() {
      if (this.commands.length <= 0) {
        return 0;
      }

      return this.commands[this.commands.length - 1].task === Constants.TASK_FORWARD ? 0 : 1;
    },

    latestDegree() {
      // commands から自動算出する
      let degree = 0;

      if (this.commands.length >= 2) {
        const current = this.commands[this.commands.length - 1];
        const prev = this.commands[this.commands.length - 2];
        degree = this.degree(Number(prev.x), Number(prev.y), Number(current.x), Number(current.y));
      }

      return this.latestDir * 180 + degree;
    },

    roboforkX() {
      // vehicles から自動算出する
      return this.vehicles.map(vehicle => {
        const commands = vehicle.vehicle_positions;

        if (commands.length <= 0) {
          return 0;
        }

        return commands[commands.length - 1].x;
      });
    },

    roboforkY() {
      // vehicles から自動算出する
      return this.vehicles.map(vehicle => {
        const commands = vehicle.vehicle_positions;

        if (commands.length <= 0) {
          return 0;
        }

        return commands[commands.length - 1].y;
      });
    },

    roboforkDegree() {
      // vehicles から自動算出する
      return this.vehicles.map(vehicle => {
        const commands = vehicle.vehicle_positions;

        if (commands.length <= 1) {
          return 0;
        }

        const prev = commands[commands.length - 2];
        const current = commands[commands.length - 1];
        const degree = this.degree(Number(prev.x), Number(prev.y), Number(current.x), Number(current.y));

        return (current.task === Constants.TASK_FORWARD ? 0 : 1) * 180 + degree;
      });
    },
  },

  updated() {
    this.updatePopoverByJQuery();
  },

  watch: {
    updateVehicles(newValues, oldValues) {
      this.vehicles.map(vehicle => {
        const newValuesIndex = newValues.findIndex(item => Number(item.id) === Number(vehicle.id));
        if (newValuesIndex !== -1) {
          // status は上書き
          vehicle.vehicle_status = newValues[newValuesIndex].vehicle_status;
          // positions は追加
          vehicle.vehicle_positions.push(...newValues[newValuesIndex].vehicle_positions);
        }

        return vehicle;
      });
    },
  },

  methods: {
    mappedX(x) {
      const offsetX = Number(x) + this.offsetX;
      return String(offsetX * this.unitX + this.width);
    },

    mappedY(y) {
      const offsetY = Number(y) + this.offsetY;
      return String(-offsetY * this.unitY);
    },

    unmappedX(x) {
      const offsetMappedX = (Number(x) - this.width) / this.unitX;
      return String(offsetMappedX - this.offsetX);
    },

    unmappedY(y) {
      const offsetMappedY = -Number(y) / this.unitY;
      return String(offsetMappedY - this.offsetY);
    },

    degree(aX, aY, bX, bY) {
      return Math.atan2(bX - aX, bY - aY) * 180 / Math.PI;
    },

    isLatest(id) {
      if (this.commands.length <= 0) {
        return false;
      }

      return this.commands[this.commands.length - 1].id === id;
    },

    isSelectedCommand(id) {
      return id === this.selectedCommandIndex;
    },

    updatePopoverByJQuery() {
      // リアクティブな要素に反応できないので、予め全部消して作り直す
      $('.map-draw-layer .popover').remove();

      // DOM が更新されたとき、TwitterBootstrap の popover を jQuery 経由で呼ぶ
      $('[data-toggle="popover"]').each((_, element) => {
        $(element).popover('destroy');
        $(element).popover('show');

        const popoverTarget = $(element).attr('aria-describedby');
        const statusCode = Number($(element).attr('data-status-code'));

        $(`#${popoverTarget}`).addClass(Constants.STATUS_CODE_CLASSNAMES[statusCode]);
      });
    },
  },
}
</script>

<style scoped>
.map-container {
  position: relative;
}

.map-image {
  width: 100%;
  height: 100%;
  position: relative;
}

.map-draw-layer {
  width: 100%;
  height: 100%;
  position: absolute;
  left: 0;
  top: 0;
}

.map-draw-layer .node {
  width: 4px;
  height: 4px;
  position: absolute;
  left: 0;
  top: 0;
  margin: -2px 0 0 -2px;
  background: yellow;
  border-radius: 2px;
  opacity: 0.5;
}

.map-draw-layer .robofork {
  width: 30px;
  height: 30px;
  position: absolute;
  left: 0;
  top: 0;
  margin: -15px 0 0 -15px;
}

.map-draw-layer .robofork img {
  transform-origin: 50% 50%;
}

</style>

<style>
/* outer component styles */
.popover.my-warning {
  background-color: #f0ad4e;
  color: #fff;
}

.popover.my-warning.top > .arrow:after {
  border-top-color: #f0ad4e;
}

.popover.my-warning .popover-title {
  background-color: #f0ad4e;
}

.popover.my-danger {
  background-color: #d9534f;
  color: #fff;
}

.popover.my-danger.top > .arrow:after {
  border-top-color: #d9534f;
}

.popover.my-danger .popover-title {
  background-color: #d9534f;
}
</style>
