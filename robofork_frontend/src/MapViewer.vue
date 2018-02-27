<template>
  <div class="container-fluid">
    <div class="row">
      <div class="map-container" :style="containerStyles">
        <img v-if="config" class="map-image" :src="config.imageUrl">
        <svg class="map-draw-layer">
          <!-- subNodes -->
          <template v-for="subNode in subNodes">
          <circle
          v-for="node in subNode.nodes"
          v-if="showAll || animate"
          :cx="mappedX(node.x)"
          :cy="mappedY(node.y)"
          class="subnode"
          :title="node.id">
          </circle>
          </template>

          <!-- mainNodes -->
          <circle
          v-for="node in mainNodes"
          :cx="mappedX(node.x)"
          :cy="mappedY(node.y)"
          @click="select(node)"
          :class="{
          current: isCurrent(node.id),
          neighbor: isNeighbor(node.id),
          }"
          :title="node.id">
          </circle>

          <!-- roboork -->
          <image
          v-if="animate"
          class="self"
          :class="{ animate: animate }"
          transform="translate(-15, -15)"
          xlink:href="/static/robofork_app/img/robofork.svg"
          :x="mappedX(robofork.x)"
          :y="mappedY(robofork.y)"
          width="30"
          height="30" />
        </svg>
      </div>
    </div>
    <div class="row">
      <div class="btn-group">
        <button @click="undo()" :disabled="!hasUndo" class="btn btn-default">undo</button>
        <button @click="redo()" :disabled="!hasRedo" class="btn btn-default">redo</button>
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
        <p>currentId: {{ currentId }}</p>
        <p>hasUndo: {{ hasUndo }}</p>
        <p>hasRedo: {{ hasRedo }}</p>
        <p>selectedNodes: {{ selectedNodes.map(n => n.id).join(', ') }}</p>
        <p>routes: {{ routes.map(i => i.id).join(', ') }}</p>
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
      robofork: {
        x: 0,
        y: 0,
      },
    }
  },

  computed: {
    containerStyles: function() {
      return {
        width: `${this.config.imageWidth}px`,
        height: `${this.config.imageHeight}px`,
      };
    },

    unitX: function() {
      return this.config.imageWidth / Number(this.config.scaleX);
    },

    unitY: function() {
      return this.config.imageHeight / Number(this.config.scaleY);
    },

    startNode: function() {
      return this.mainNodes.find(item => item.id === this.config.startId);
    },

    currentId: function() {
      return this.selectedNodes.length > 0 ? this.selectedNodes[this.selectedNodes.length - 1].id : this.config.startId;
    },

    // selectedNodes から subNodes 含めたノードリストを自動計算する
    routes: function() {
      if (!this.startNode) {
        return [];
      }
      if (this.selectedNodes.length <= 0) {
        return [this.startNode];
      }

      const mainNodeIds = [this.config.startId, ...this.selectedNodes.map(item => item.id)];

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
  },

  created() {
    this.$watch('loaded', () => {
      if (this.loaded) {
        this.initialize();
      }
    });

    // routes の変更を検知して parentRoutes も変更する
    this.$watch('routes', () => {
      this.$emit('update:parentRoutes', this.routes);
    });
  },

  methods: {
    initialize: function() {
      this.selectedNodes = [];

      this.history.clear();
      // history のバインディングできないところを callback でカバー
      this.history.setCallback(() => {
        this.hasUndo = this.history.hasUndo();
        this.hasRedo = this.history.hasRedo();
      });

      this.robofork.x = this.startNode.x;
      this.robofork.y = this.startNode.y;
    },

    add: function(node) {
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

    select: function(node) {
      // 現在のノードか隣り合ったノードのどちらでもない場合
      if (!this.isCurrent(node.id) && !this.isNeighbor(node.id)) {
        return;
      }

      // アニメーション途中は選択できない
      if (this.animate) {
        return;
      }

      this.add(this.mainNodes.find(item => item.id === node.id));
    },

    undo: function() {
      this.history.undo();
    },

    redo: function() {
      this.history.redo();
    },

    clear: function() {
      this.initialize();
    },

    mappedX: function(x) {
      const offsetX = Number(x) + Number(this.config.offsetX);
      return String(offsetX * this.unitX + this.config.imageWidth);
    },

    mappedY: function(y) {
      const offsetY = Number(y) + Number(this.config.offsetY);
      return String(-offsetY * this.unitY);
    },

    isCurrent: function(id) {
      return this.currentId === id;
    },

    isNeighbor: function(id) {
      const targetNode = this.mainNodes.find(item => item.id === this.currentId);
      if (!targetNode) {
        return false;
      }
      return targetNode.neighbors.includes(id);
    },

    start: function() {
      this.animate = true;
      this.animateTimer = null;

      let animatePointer = 0;
      this.animateTimer = setInterval(() => {
        if (animatePointer >= this.routes.length) {
          setTimeout(this.stop, 1000);
          return;
        }

        this.robofork.x = this.routes[animatePointer].x;
        this.robofork.y = this.routes[animatePointer].y;

        animatePointer++;
      }, 100);
    },

    stop: function() {
      clearInterval(this.animateTimer);
      this.animate = false;
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

.map-draw-layer g {
  width: 100%;
  height: 100%;
}
.map-draw-layer circle {
  r: 8;
  fill: blue;
  opacity: 0.5;
  cursor: default;
}

.map-draw-layer circle.current {
  fill: red;
  opacity: 1;
  cursor: pointer;
}

.map-draw-layer circle.neighbor {
  opacity: 1;
  cursor: pointer;
}

.map-draw-layer circle.subnode {
  r: 4;
  fill: yellow;
}

.map-draw-layer circle.current-path {
  fill: red;
}

.map-draw-layer .self {
}

.map-draw-layer .self.animate {
  transition: x linear 100ms, y linear 100ms;
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
