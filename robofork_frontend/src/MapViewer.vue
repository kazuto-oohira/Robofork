<template>
  <div class="container-fluid" id="map-viewer">
    <div class="row">
      <div class="map-container"
        :style="{ width: `${width}px`, height: `${height}px` }"
        @click.self="mark($event.offsetX, $event.offsetY)"
      >
        <img v-if="imageUrl" class="map-image" :src="imageUrl">
        <div class="map-draw-layer">
          <!-- subNodes -->
          <template v-for="subNode in subNodes">
          <div
            v-for="node in subNode.nodes"
            v-if="enableSubNodes"
            class="subnode"
            :style="{
              transform: `translate(${mappedX(node.x)}px, ${mappedY(node.y)}px)`
            }"
            :title="node.id"
          ></div>
          </template>

          <!-- mainNodes -->
          <div
            v-for="node in mainNodes"
            class="mainnode"
            :class="{
              current: isCurrent(node.id),
            }"
            :style="{
              transform: `translate(${mappedX(node.x)}px, ${mappedY(node.y)}px)`
            }"
            :title="node.id"
          >
            <img
              src="/static/robofork_app/img/robofork.svg"
              alt=""
              width="30"
              height="30"
              v-if="isCurrent(node.id)"
              :style="{
                transform: `rotate(${currentDegree}deg)`
              }"
            >
          </div>

          <!-- roboork -->
          <div
            class="robofork"
            :class="{ animate: enableRobofork }"
            :style="{
              transform: `translate(${mappedX(roboforkX)}px, ${mappedY(roboforkY)}px)`
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
    <div class="row">
      <div class="checkbox">
        <label>
          <input type="checkbox" v-model="checkSubNodes"> サブノードも含めて表示する
        </label>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'map-viewer',

  props: [
    'width',
    'height',
    'scaleX',
    'scaleY',
    'offsetX',
    'offsetY',
    'imageUrl',
    'routes',
    'mainNodes',
    'subNodes',
    'animate',
    'animateIndex',
  ],

  data() {
    return {
      checkSubNodes: true,
    }
  },

  computed: {
    enableSubNodes() {
      return this.checkSubNodes || this.animate;
    },

    enableRobofork() {
      return !!this.animate;
    },

    unitX() {
      return this.width / this.scaleX;
    },

    unitY() {
      return this.height / this.scaleY;
    },

    currentDir() {
      if (this.mainNodes.length <= 0) {
        return 0;
      }

      return this.mainNodes[this.mainNodes.length - 1].dir;
    },

    currentDegree() {
      // routes から自動算出する
      let degree = 0;

      if (this.routes.length >= 2) {
        const current = this.routes[this.routes.length - 1];
        const prev = this.routes[this.routes.length - 2];
        degree = this.degree(Number(prev.x), Number(prev.y), Number(current.x), Number(current.y));
      }

      return this.currentDir * 180 + degree;
    },

    roboforkX() {
      // routes, animateIndex から自動算出する
      if (this.routes.length <= 0) {
        return 0;
      }
      if (!this.animate) {
        return this.routes[0].x;
      }

      return this.routes[this.animateIndex].x;
    },

    roboforkY() {
      // routes, animateIndex から自動算出する
      if (this.routes.length <= 0) {
        return 0;
      }
      if (!this.animate) {
        return this.routes[0].y;
      }

      return this.routes[this.animateIndex].y;
    },

    roboforkDegree() {
      // routes, animateIndex から自動算出する
      if (!this.animate || this.animateIndex === null || this.routes.length <= 1) {
        return 0;
      }

      let prev, current;

      if (this.animateIndex === 0) {
        prev = this.routes[this.animateIndex];
        current = this.routes[this.animateIndex + 1];
      } else if (this.routes.length - 1 <= this.animateIndex) {
        prev = this.routes[this.routes.length - 2];
        current = this.routes[this.routes.length - 1];
      } else {
        prev = this.routes[this.animateIndex - 1];
        current = this.routes[this.animateIndex];
      }

      const degree = this.degree(Number(prev.x), Number(prev.y), Number(current.x), Number(current.y));

      return current.dir * 180 + degree;
    },
  },

  methods: {
    mark(x, y) {
      this.$emit('addMark', {
        x: this.unmappedX(x),
        y: this.unmappedY(y),
      });
    },

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

    isCurrent(id) {
      if (this.mainNodes.length <= 0) {
        return false;
      }

      return this.mainNodes[this.mainNodes.length - 1].id === id;
    },
  },
}
</script>

<style scoped>
.map-container {
  position: relative;
}

.map-container:after {
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

.map-draw-layer .mainnode {
  width: 16px;
  height: 16px;
  position: absolute;
  left: 0;
  top: 0;
  margin: -8px 0 0 -8px;
  background: blue;
  border-radius: 8px;
  opacity: 1;
}

.map-draw-layer .mainnode.current {
  width: 30px;
  height: 30px;
  margin: -15px 0 0 -15px;
  background: transparent;
  border-radius: 15px;
}
.map-draw-layer .mainnode.current img {
  transform-origin: 50% 50%;
}

.map-draw-layer .subnode {
  width: 8px;
  height: 8px;
  position: absolute;
  left: 0;
  top: 0;
  margin: -4px 0 0 -4px;
  background: yellow;
  border-radius: 4px;
  opacity: 0.5;
}

.map-draw-layer .robofork {
  width: 30px;
  height: 30px;
  position: absolute;
  left: 0;
  top: 0;
  display: none;
  margin: -15px 0 0 -15px;
}

.map-draw-layer .robofork img {
  transform-origin: 50% 50%;
}

.map-draw-layer .robofork.animate {
  display: block;
  transition: transform linear 100ms;
}

.map-draw-layer .robofork img {
  transform-origin: 50% 50%;
}
</style>
