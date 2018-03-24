<template>
  <div id="map-viewer">
    <div class="row">
      <div class="col-md-8">
        <div class="map-container"
          :style="{ width: `${width}px`, height: `${height}px` }"
          :class="{
            'routing': enableRouting,
            'point-edit': enablePointEdit,
          }"
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
              draggable="true"
              :class="{
                latest: isLatest(node.id),
                selected: isSelectedCommand(node.id),
              }"
              :style="{
                transform: `translate(${mappedX(node.x)}px, ${mappedY(node.y)}px)`
              }"
              :title="node.id"
              @mousedown.self="select(node.id)"
              @dragend="move($event, mappedX(node.x), mappedY(node.y), node.id)"
            >
              <img
                src="/static/robofork_app/img/robofork.svg"
                alt=""
                width="30"
                height="30"
                v-if="isLatest(node.id)"
                :style="{
                  transform: `rotate(${latestDegree}deg)`
                }"
              >
            </div>

            <!-- roboork -->
            <div
              class="robofork"
              :class="{ animate: enableRobofork }"
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
      <!--
      <div class="col-md-4">
        <div class="checkbox">
          <label>
            <input type="checkbox" v-model="checkSubNodes"> サブノードも含めて表示する
          </label>
        </div>
      </div>
      -->
      <div class="col-md-4 btn-group">
        <div class="row">
          <div class="col-md-12 btn-group">
            <button
              class="btn btn-default"
              :class="{ 'btn-primary': enableRouting }"
              @click="selectRouting"
            >ルート追加モード</button>
            <button
              class="btn btn-default"
              :class="{ 'btn-primary': enablePointEdit }"
              @click="selectPointEdit"
            >ポイント編集モード</button>
          </div>
          <div class="col-md-12">
            <div class="checkbox">
              <label>
                <input type="checkbox" :disabled="disableNormalization" v-model="checkNormalization">
                45度単位でマップ上にポイントする
              </label>
            </div>
          </div>

        </div>
        <hr>
        <div class="row">
          <div class="col-md-12">
            <p>次の進行方向</p>
            <div class="btn-group">
              <button
                class="btn btn-default"
                :class="{ 'btn-primary': enableForwardDir }"
                @click="changeDir(true)"
                :disabled="disableChangeDir"
              >{{ labelDirForward }}</button>
              <button
                class="btn btn-default"
                :class="{ 'btn-primary': enableReverseDir }"
                @click="changeDir(false)"
                :disabled="disableChangeDir"
                >{{ labelDirReverse }}</button>
            </div>
          </div>
        </div>
        <hr>
        <div class="row">
          <div class="col-md-12 btn-group">
            <button @click="start()" :disabled="disableStart" class="btn btn-warning">シミュレーション開始</button>
            <button @click="stop()" :disabled="disableStop" class="btn btn-default">停止</button>
          </div>
        </div>
        <hr>
        <div class="row">
          <div class="col-md-12">
            <button @click="clear()":disabled="disableClear" class="btn btn-danger">ルートを全て削除する</button>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script>
import * as Constants from './Constants'

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
    'commands',
    'mainNodes',
    'subNodes',
    'animate',
    'animateIndex',
    'selectedCommandIndex',
    'hasCommands',
    'currentDir',
  ],

  data() {
    return {
      checkSubNodes: true,
      checkNormalization: true,
      modeIndex: 0,
      animationSpeed: Constants.ANIMATION_SPEED,
      labelDirForward: Constants.DIR_FORWARD,
      labelDirReverse: Constants.DIR_REVERSE,
    }
  },

  computed: {
    enableSubNodes() {
      return this.checkSubNodes || this.animate;
    },

    enableRobofork() {
      return !!this.animate;
    },

    enableRouting() {
      return this.modeIndex === Constants.MODE_ROUTING;
    },

    enablePointEdit() {
      return this.modeIndex === Constants.MODE_POINT_EDIT;
    },

    enableForwardDir() {
      return !!this.currentDir;
    },

    enableReverseDir() {
      return !this.currentDir;
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
      // commands, animateIndex から自動算出する
      if (this.commands.length <= 0) {
        return 0;
      }
      if (!this.animate) {
        return this.commands[0].x;
      }

      return this.commands[this.animateIndex].x;
    },

    roboforkY() {
      // commands, animateIndex から自動算出する
      if (this.commands.length <= 0) {
        return 0;
      }
      if (!this.animate) {
        return this.commands[0].y;
      }

      return this.commands[this.animateIndex].y;
    },

    roboforkDegree() {
      // commands, animateIndex から自動算出する
      if (!this.animate || this.animateIndex === null || this.commands.length <= 1) {
        return 0;
      }

      let prev, current;

      if (this.animateIndex === 0) {
        prev = this.commands[this.animateIndex];
        current = this.commands[this.animateIndex + 1];
      } else if (this.commands.length - 1 <= this.animateIndex) {
        prev = this.commands[this.commands.length - 2];
        current = this.commands[this.commands.length - 1];
      } else {
        prev = this.commands[this.animateIndex - 1];
        current = this.commands[this.animateIndex];
      }

      const degree = this.degree(Number(prev.x), Number(prev.y), Number(current.x), Number(current.y));

      return (current.task === Constants.TASK_FORWARD ? 0 : 1) * 180 + degree;
    },

    disableNormalization() {
      return this.modeIndex !== Constants.MODE_ROUTING;
    },

    disableClear() {
      return !this.hasCommands;
    },

    disableStart() {
      return !this.hasCommands || this.animate;
    },

    disableStop() {
      return !this.hasCommands || !this.animate;
    },

    disableChangeDir() {
      return !this.hasCommands || this.animate || (this.modeIndex !== Constants.MODE_ROUTING);
    },
  },

  methods: {
    mark(x, y) {
      // ルート追加モードでなければマップを選択しても何もしない
      if (this.modeIndex !== Constants.MODE_ROUTING) {
        return;
      }

      // 45度単位の座標の正規化を必要に応じて行う
      if (this.checkNormalization) {
        const prevX = Number(this.mappedX(this.mainNodes[this.mainNodes.length - 1].x));
        const prevY = Number(this.mappedY(this.mainNodes[this.mainNodes.length - 1].y));

        [ x, y ] = this.normalize(prevX, prevY, x, y);
      }

      this.$emit('addMark', {
        x: this.unmappedX(x),
        y: this.unmappedY(y),
      });
    },

    select(id) {
      this.$emit('update:selectedCommandIndex', id);
    },

    move(event, originX, originY, id) {
      const rect = event.target.getBoundingClientRect();
      const newX = Number(originX) + event.offsetX - (rect.width / 2);
      const newY = Number(originY) + event.offsetY - (rect.height / 2);
      this.$emit('updateMark', id, {
        x: this.unmappedX(newX),
        y: this.unmappedY(newY),
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

    normalize(pX, pY, cX, cY) {
      const width = Number(cX) - Number(pX);
      const height = Number(cY) - Number(pY);
      const degree = Math.atan2(width, height) * 180 / Math.PI;
      const hypotenuse = Math.sqrt(width ** 2 + height ** 2);

      // normalize each 45 degrees
      const normalizedDegree = Math.round(degree / 45) * 45;
      const nX = pX + hypotenuse * Math.sin(normalizedDegree * Math.PI / 180);
      const nY = pY + hypotenuse * Math.cos(normalizedDegree * Math.PI / 180);

      return [nX, nY];
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

    selectRouting() {
      this.modeIndex = Constants.MODE_ROUTING;
    },

    selectPointEdit() {
      this.modeIndex = Constants.MODE_POINT_EDIT;
    },

    clear() {
      this.$emit('clear');
    },

    start() {
      this.$emit('start');
    },

    stop() {
      this.$emit('stop');
    },

    changeDir(nextDir) {
      if (nextDir === this.currentDir) {
        return;
      }

      this.$emit('reverse');
    },
  },
}
</script>

<style scoped>
#map-viewer > .row > .col-md-8 {
  background-color: #8c8c8c;
}
.map-container {
  position: relative;
  margin: 0 auto;
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
  cursor: pointer;
}

.map-draw-layer .mainnode.latest img {
  width: 30px;
  height: 30px;
  position: absolute;
  left: 8px;
  top: 8px;
  margin: -15px 0 0 -15px;
  transform-origin: 50% 50%;
}

.map-container.point-edit .map-draw-layer .mainnode.selected {
  background: red;
}

.map-container.point-edit .map-draw-layer .mainnode.latest img {
  display: none;
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

.checkbox label {
  user-select: none;
}
</style>
