<template>
  <div class="container-fluid" id="map-multi-viewer">
    <div class="row">
      <div class="map-container"
        :style="{ width: `${width}px`, height: `${height}px` }"
      >
        <img v-if="imageUrl" class="map-image" :src="imageUrl">
        <div class="map-draw-layer">
          <!-- commands -->
          <div
            v-for="command in commands"
            class="node"
            :style="{
              transform: `translate(${mappedX(command.x)}px, ${mappedY(command.y)}px)`
            }"
          ></div>

          <!-- roboork -->
          <div
          v-if="commands.length > 0"
            class="robofork"
            :style="{
              transform: `translate(${mappedX(roboforkX)}px, ${mappedY(roboforkY)}px)`,
              'transition-duration': `${animationSpeed}ms`
            }"
          >
            <img
              src="/static/robofork_app/img/robofork.svg"
              alt=""
              width="30"
              height="30"
              :style="{
                transform: `rotate(${roboforkDegree}deg)`
              }"
            >
          </div>
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
    'positions',
  ],

  data() {
    return {
      animationSpeed: Constants.ANIMATION_SPEED,
    }
  },

  computed: {
    commands() {
      if (!this.positions) {
        return [];
      }

      return this.positions;
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
      // commands から自動算出する
      if (this.commands.length <= 0) {
        return 0;
      }

      return this.commands[this.commands.length - 1].x;
    },

    roboforkY() {
      // commands から自動算出する
      if (this.commands.length <= 0) {
        return 0;
      }

      return this.commands[this.commands.length - 1].y;
    },

    roboforkDegree() {
      // commands から自動算出する
      if (this.commands.length <= 1) {
        return 0;
      }

      const prev = this.commands[this.commands.length - 2];
      const current = this.commands[this.commands.length - 1];
      const degree = this.degree(Number(prev.x), Number(prev.y), Number(current.x), Number(current.y));

      return (current.task === Constants.TASK_FORWARD ? 0 : 1) * 180 + degree;
    },
  },

  created() {
    console.log('created');
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
  },
}
</script>

<style scoped>
.map-container {
  position: relative;
}

.map-container.routing:after {
  width: 100%;
  height: 100%;
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  z-index: 100;
  display: block;
  background: rgba(0, 0, 0, 0);
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
