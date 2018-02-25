<template>
  <div class="container-fluid">
    <div class="row">
      <div class="map-container" :style="containerStyles">
        <img v-if="config" class="map-image" :src="config.imageUrl">
        <svg class="map-draw-layer">
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
      <h3>履歴操作</h3>
      <button @click="undo()" :disabled="!hasUndo" class="btn btn-default">undo</button>
      <button @click="redo()" :disabled="!hasRedo" class="btn btn-default">redo</button>
      <button @click="clear()":disabled="selectedNodes.length <= 0" class="btn btn-warning">clear</button>
    </div>
    <div class="row">
      <div class="log col-sm-12">
        <p>currentId: {{ currentId }}</p>
        <p>selectedNodes: {{ selectedNodes.map(n => n.id).join(',') }}</p>
        <p>hasUndo: {{ hasUndo }}</p>
        <p>hasRedo: {{ hasRedo }}</p>
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
      config: {},
      selectedNodes: [],
      hasUndo: false,
      hasRedo: false,
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
.map-container {
  position: relative;
  select: none;
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

.log {
  height: 100px;
  box-sizing: border-box;
  overflow: scroll;
  margin-top: 20px;
  padding: 0.5rem 1rem;
  background: #eee;
}

.log p {
  margin: 0;
  line-height: 1.0;
}
</style>
