<template>
  <div class="container-fluid">
    <div class="row">
      <div class="map-container" :style="containerStyles">
        <img v-if="config" class="map-image" :src="config.imageUrl">
        <svg class="map-draw-layer">
          <circle
          v-for="(node, index) in allnodes"
          v-if="showAll"
          :cx="mapSubX[index]"
          :cy="mapSubY[index]"
          class="subnode"
          :title="node.id">
          </circle>
          <circle
          v-for="(node, index) in mainNodes"
          :cx="mapX[index]"
          :cy="mapY[index]"
          @click="click(node)"
          :class="{
          current: isCurrent(node.id),
          neighbor: isNeighbor(node.id),
          }"
          :title="node.id">
          </circle>
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
        <button @click="startAnimation()" class="btn btn-primary">Start</button>
        <button @click="startAnimation()" class="btn btn-danger">Stop</button>
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
        <p>currentId: {{ currentId }}</p>
        <p>selectedNodes: {{ selectedNodes.map(n => n.id).join(',') }}</p>
        <p>hasUndo: {{ hasUndo }}</p>
        <p>hasRedo: {{ hasRedo }}</p>
        <p>allnodes: {{ allnodes }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import undo from 'undo-manager'

const OPERATION_ENDPOINT = '/static/robofork_app/api/operation_control.json';

export default {
  name: 'map-viewer',

  data() {
    return {
      mainNodes: [],
      subNodes: [],
      config: {},
      selectedNodes: [],
      hasUndo: false,
      hasRedo: false,
      showAll: false,
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

    mapX: function() {
      return this.mainNodes.map((item) => {
        const offsetX = Number(item.x) + Number(this.config.offsetX);
        return offsetX * this.unitX + this.config.imageWidth;
      });
    },

    mapY: function() {
      return this.mainNodes.map((item) => {
        const offsetY = Number(item.y) + Number(this.config.offsetY);
        return -offsetY * this.unitY;
      });
    },

    mapSubX: function() {
      return this.allnodes.map((item) => {
        const offsetX = Number(item.x) + Number(this.config.offsetX);
        return offsetX * this.unitX + this.config.imageWidth;
      });
    },

    mapSubY: function() {
      return this.allnodes.map((item) => {
        const offsetY = Number(item.y) + Number(this.config.offsetY);
        return -offsetY * this.unitY;
      });
    },

    allnodes: function() {
      return this.mainNodes.concat(...this.subNodes.map(item => item.nodes)).sort((a, b) => a.id - b.id);
    },

    currentId: function() {
      return this.selectedNodes.length > 0 ? this.selectedNodes[this.selectedNodes.length - 1].id : this.config.startNode;
    },
  },

  created() {
    this.history = new undo();

    axios.get(OPERATION_ENDPOINT)
      .then((resp) => {
        if ('config' in resp.data) {
          this.config = resp.data.config;
        }
        if ('mainNodes' in resp.data) {
          this.mainNodes = resp.data.mainNodes;
        }
        if ('subNodes' in resp.data) {
          this.subNodes = resp.data.subNodes;
        }

        this.initialize();

        // history のバインディングできないところを callback でカバー
        this.history.setCallback(() => {
          this.hasUndo = this.history.hasUndo();
          this.hasRedo = this.history.hasRedo();
        });
      });
  },

  methods: {
    initialize: function() {
      this.selectedNodes = [];
      this.history.clear();
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

    click: function(node) {
      if (!this.isCurrent(node.id) && !this.isNeighbor(node.id)) {
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
  },
}
</script>

<style>
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
