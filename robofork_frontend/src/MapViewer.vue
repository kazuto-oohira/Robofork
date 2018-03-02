<template>
  <div class="container-fluid">
    <div class="row">
      <div class="map-container" :style="containerStyles">
        <img v-if="config" class="map-image" :src="config.imageUrl">
        <div class="map-draw-layer" @click="mark($event.offsetX, $event.offsetY)">
          <!-- subNodes -->
          <template v-for="subNode in subNodes">
          <div
            v-for="node in subNode.nodes"
            v-if="showAll || animate"
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
          ></div>

          <!-- roboork -->
          <div
            v-if="animate"
            class="robofork"
            :class="{ animate: animate }"
            :style="{
              left: `${mappedX(robofork.x)}px`,
              top: `${mappedY(robofork.y)}px`
            }"
          >
            <img
              src="/static/robofork_app/img/robofork.svg"
              alt=""
              width="30"
              height="30"
              :style="{
                transform: `rotate(${degree}deg)`
              }"
            >
          </div>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="btn-group">
        <button @click="undo()" :disabled="!hasUndo || animate" class="btn btn-default">undo</button>
        <button @click="redo()" :disabled="!hasRedo || animate" class="btn btn-default">redo</button>
        <button @click="clear()":disabled="selectedNodes.length <= 0" class="btn btn-warning">clear</button>
      </div>
      <div class="btn-group">
        <button @click="start()" :disabled="animate" class="btn btn-primary">Start</button>
        <button @click="stop()" :disabled="!animate" class="btn btn-danger">Stop</button>
      </div>
    </div>
    <div class="row">
      <div class="checkbox">
        <label>
          <input type="checkbox" v-model="showAll"> サブノードも含めて表示する
        </label>
      </div>
    </div>
    <div class="row">
      <div class="log col-sm-12">
        <p>startNode: {{ startNode }}</p>
        <p>currentNode: {{ currentNode }}</p>
        <p>currentId: {{ currentId }}</p>
        <p>hasUndo: {{ hasUndo }}</p>
        <p>hasRedo: {{ hasRedo }}</p>
        <p>selectedNodes: {{ selectedNodes.map(n => n.id).join(', ') }}</p>
        <p>routes: {{ routes.map(i => i.id).join(', ') }}</p>
        <p>subNodes: {{ subNodes }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'map-viewer',

  props: [
    'mainNodes',
    'subNodes',
    'config',
    'history',
    'parentRoutes',
    'loaded',
  ],

  data() {
    return {
      selectedNodes: [],
      hasUndo: false,
      hasRedo: false,
      showAll: false,
      animate: false,
      animatePointer: null,
      robofork: {
        x: 0,
        y: 0,
      },
    }
  },

  computed: {
    containerStyles() {
      return {
        width: `${this.config.imageWidth}px`,
        height: `${this.config.imageHeight}px`,
      };
    },

    unitX() {
      return this.config.imageWidth / Number(this.config.scaleX);
    },

    unitY() {
      return this.config.imageHeight / Number(this.config.scaleY);
    },

    startNode() {
      return this.mainNodes.find(item => item.id === this.config.startId);
    },

    currentNode() {
      return this.selectedNodes.length > 0 ? this.selectedNodes[this.selectedNodes.length - 1] : null;
    },

    currentId() {
      return this.selectedNodes.length > 0 ? this.selectedNodes[this.selectedNodes.length - 1].id : null;
    },

    // selectedNodes から subNodes 含めたノードリストを自動計算する
    routes() {
      if (!this.startNode) {
        return [];
      }
      if (this.selectedNodes.length <= 0) {
        return [this.startNode];
      }

      const mainNodeIds = this.selectedNodes.map(item => item.id);

      let nodes = [this.startNode];

      mainNodeIds.reduce((prev, current) => {
        const subNode = this.subNodes.find(item => item.path.includes(current) && item.path.includes(prev));

        if (!subNode) {
          console.error(`subNode is not found: path = ${[prev, current]}`);
        }

        if (current === subNode.path[1]) {
          // forward
          // array#sort などでソートしても、バインディングな要素で内部で入れ替えなどが発生するため、一度複製する
          nodes.push(...Object.assign([], subNode.nodes));
        } else {
          // reverse
          nodes.push(...Object.assign([], subNode.nodes).reverse());
        }

        // mainNode
        nodes.push(this.mainNodes.find(item => item.id === current));

        return current;
      });

      return nodes;
    },

    degree() {
      if (!this.animate || !this.animatePointer) {
        return 90;
      }

      let prev = this.routes[this.animatePointer - 1];
      let current = this.routes[this.animatePointer];

      if (this.routes.length <= this.animatePointer) {
        prev = this.routes[this.routes.length - 2]
        current = this.routes[this.routes.length - 1]
      }

      return this.config.startDir * 90 + 90 + Math.atan2(current.x - prev.x, current.y - prev.y) * 180 / Math.PI;
    },
  },

  created() {
    this.$watch('loaded', () => {
      if (this.loaded) {
        this.initialize();
      }
    });

    // mainNodes の変更を検知して、App.vue 側の mainNodes も変更する
    this.$watch('mainNodes', () => {
      this.$emit('update:mainNodes', this.mainNodes);
    });

    // routes の変更を検知して parentRoutes も変更する
    this.$watch('routes', () => {
      this.$emit('update:parentRoutes', this.routes);
    });
  },

  methods: {
    initialize() {
      this.nodeId = 0;
      this.selectedNodes = [];

      this.history.clear();
      // history のバインディングできないところを callback でカバー
      this.history.setCallback(() => {
        this.hasUndo = this.history.hasUndo();
        this.hasRedo = this.history.hasRedo();
      });

      this.robofork.x = 0;// this.startNode.x;
      this.robofork.y = 0;// this.startNode.y;
    },

    add(node) {
      this.selectedNodes.push(node);

      this.history.add({
        undo: () => {
          this.selectedNodes.pop()
        },
        redo: () => {
          this.selectedNodes.push(node);
        },
      });
    },

    generateId() {
      return this.nodeId++;
    },

    mark(x, y) {
      const markedX = this.unmappedX(x);
      const markedY = this.unmappedY(y);

      let nodes;
      if (this.mainNodes.length > 0) {
        nodes = this.path(this.currentNode.x, this.currentNode.y, markedX, markedY);
      }

      const newNode = {
        id: this.generateId(),
        x: markedX,
        y: markedY
      };

      this.mainNodes.push(newNode);
      if (nodes) {
        this.subNodes.push({
          path: [this.currentNode.id, newNode.id],
          nodes: nodes
        });
      }
      this.add(newNode);
    },

    path(startX, startY, endX, endY) {
      const width = Number(endX) - Number(startX);
      const height = Number(endY) - Number(startY);
      const hypotenuse = Math.sqrt(width ** 2 + height ** 2);

      const unitX = 0.1 * width / hypotenuse;
      const unitY = 0.1 * height / hypotenuse;

      let subNodes = [];
      let diffX = 0;
      let diffY = 0;
      while(Math.abs(diffX) < Math.abs(width) && Math.abs(diffY) < Math.abs(height)) {
        subNodes.push(
          {
            id: this.generateId(),
            x: Number(startX) + diffX,
            y: Number(startY) + diffY,
          }
        );
        diffX += unitX;
        diffY += unitY;
      }
      return subNodes;
    },

    undo() {
      // アニメーション途中は選択できない
      if (this.animate) {
        return;
      }

      this.history.undo();
    },

    redo() {
      // アニメーション途中は選択できない
      if (this.animate) {
        return;
      }

      this.history.redo();
    },

    clear() {
      this.animate = false;
      this.initialize();
    },

    mappedX(x) {
      const offsetX = Number(x) + Number(this.config.offsetX);
      return String(offsetX * this.unitX + this.config.imageWidth);
    },

    mappedY(y) {
      const offsetY = Number(y) + Number(this.config.offsetY);
      return String(-offsetY * this.unitY);
    },

    unmappedX(x) {
      const offsetMappedX = (Number(x) - this.config.imageWidth) / this.unitX;
      return String(offsetMappedX - Number(this.config.offsetX));
    },

    unmappedY(y) {
      const offsetMappedY = -Number(y) / this.unitY;
      return String(offsetMappedY - Number(this.config.offsetY));
    },

    isCurrent(id) {
      return this.currentId === id;
    },

    start() {
      this.robofork.x = this.startNode.x;
      this.robofork.y = this.startNode.y;

      this.animate = true;
      this.animatePointer = 0;
      this.animateTimer = null;

      this.animateTimer = setInterval(() => {
        if (this.animatePointer >= this.routes.length) {
          setTimeout(this.stop, 1000);
          return;
        }

        this.robofork.x = this.routes[this.animatePointer].x;
        this.robofork.y = this.routes[this.animatePointer].y;

        this.animatePointer++;
      }, 100);
    },

    stop() {
      clearInterval(this.animateTimer);
      this.animate = false;
      this.animatePointer = null;
      this.robofork.x = this.startNode.x;
      this.robofork.y = this.startNode.y;
    },
  },
}
</script>

<style scoped>
.row {
  margin-bottom: 20px;
}

.map-container {
  position: relative;
  user-select: none;
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
  background: red;
  opacity: 1;
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
  transform: translate(-15px, -15px);
}

.map-draw-layer .robofork.animate {
  transition: left linear 100ms, top linear 100ms;
}

.map-draw-layer .robofork img {
  transform-origin: 50% 50%;
}

.btn-group + .btn-group {
  margin-left: 20px;
}

.checkbox label {
  user-select: none;
}

.log {
  height: 100px;
  box-sizing: border-box;
  overflow: scroll;
  padding: 0.5rem 1rem;
  background: #eee;
}

.log p {
  margin: 0;
  line-height: 1.0;
}
</style>
