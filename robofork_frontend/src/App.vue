<template>
  <div class="container operation-plan-detail">
    <div class="row">
      <div class="col-xs-6">
        <h2>マップ画面</h2>
        <map-viewer
          :width="config.imageWidth"
          :height="config.imageHeight"
          :scaleX="Number(config.scaleX)"
          :scaleY="Number(config.scaleY)"
          :offsetX="Number(config.offsetX)"
          :offsetY="Number(config.offsetY)"
          :imageUrl="config.imageUrl"
          :routes="routes"
          :mainNodes="mainNodes"
          :subNodes="subNodes"
          :animate="animate"
          :animateIndex="animateIndex"
          @addMark="addMark"
        ></map-viewer>
      </div>
      <div class="col-xs-6">
        <h2>指示画面</h2>
        <command-viewer
          :commands="commands"
        ></command-viewer>
      </div>
    </div>
    <div class="row">
      <div class="col-xs-6">
        <terminal
          :hasUndo="hasUndo"
          :hasRedo="hasRedo"
          :hasRoutes="this.routes.length > 0"
          :animate="animate"
          :currentDir.sync="currentDir"
          @undo="undo"
          @redo="redo"
          @clear="clear"
          @start="start"
          @stop="stop"
          @up="up"
          @down="down"
        ></terminal>

        <div class="log">
          <p>animate: {{ animate }}</p>
          <p>animateIndex: {{ animateIndex }}</p>
          <p>hasUndo: {{ hasUndo }}</p>
          <p>hasRedo: {{ hasRedo }}</p>
          <p>marks: {{ marks }}</p>
          <p>mainNodes: {{ mainNodes }}</p>
          <p>commands: {{ commands }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import undoManager from 'undo-manager'

import MapViewer from './MapViewer.vue'
import CommandViewer from './CommandViewer.vue'
import Terminal from './Terminal.vue'

const OPERATION_ENDPOINT = '/static/robofork_app/api/operation_control.json';
const START_ID = 0;

export default {
  name: 'app',
  render: h => h(this),

  components: {
    'map-viewer': MapViewer,
    'command-viewer': CommandViewer,
    'terminal': Terminal,
  },

  data () {
    return {
      config: {},
      marks: [],
      history: null,
      hasUndo: false,
      hasRedo: false,
      animate: false,
      animateIndex: 0,
      currentDir: 0,
    }
  },

  computed: {
    mainNodes() {
      // marks から自動算出する
      if (this.marks.length <= 0) {
        return [];
      }

      this.nodeId = START_ID;

      return this.marks.map(item => {
        item.id = this.generateId();
        item.isMain = true;
        return item;
      });
    },

    subNodes() {
      // mainNodes から自動算出する
      if (this.mainNodes.length <= 1) {
        return [];
      }

      let nodes = [];
      this.mainNodes.reduce((prev, current) => {
        nodes.push({
          path: [prev.id, current.id],
          nodes: this.path(prev.x, prev.y, current.x, current.y).map(item => {
            item.dir = current.dir;
            return item;
          }),
        });
        return current;
      });

      return nodes;
    },

    startNode() {
      return this.mainNodes.find(item => item.id === START_ID);
    },

    currentNode() {
      if (this.mainNodes.length <= 0) {
        return null;
      }
      return this.mainNodes[this.mainNodes.length - 1];
    },

    currentId() {
      if (this.mainNodes.length <= 0) {
        return null;
      }
      return this.mainNodes[this.mainNodes.length - 1].id;
    },

    commands() {
      // mainNodes, subNodes から自動算出する
      if (!this.startNode) {
        return [];
      }
      if (this.mainNodes.length <= 0) {
        return [this.startNode];
      }

      const mainNodeIds = this.mainNodes.map(item => item.id);

      let nodes = [this.startNode];

      mainNodeIds.reduce((prev, current) => {
        const subNode = this.subNodes.find(item => item.path.includes(current) && item.path.includes(prev));

        if (!subNode) {
          console.error(`subNode is not found: path = ${[prev, current]}`);
        }

        // subNode
        nodes.push(...subNode.nodes);

        // mainNode
        nodes.push(this.mainNodes.find(item => item.id === current));

        return current;
      });

      return nodes;
    },

    routes() {
      // commands から自動算出する（その場で行う命令をフィルタリングしたもの）
      return this.commands.filter(item => item.lift !== true);
    },
  },

  created() {
    axios.get(OPERATION_ENDPOINT)
      .then((resp) => {
        if ('config' in resp.data) {
          this.config = resp.data.config;
          this.currentDir = Number(this.config.startDir);

          if ('startX' in resp.data.config && 'startY' in resp.data.config) {
            this.addMark({
              x: resp.data.config.startX,
              y: resp.data.config.startY,
            });
          }
        }
      });

    this.history = undoManager();
    this.initialize();
  },

  methods: {
    initialize() {
      this.animate = false;
      this.marks = [];
      this.history.clear();

      // history のバインディングできないところを callback でカバー
      this.history.setCallback(() => {
        this.hasUndo = this.history.hasUndo();
        this.hasRedo = this.history.hasRedo();
      });
    },

    generateId() {
      return this.nodeId++;
    },

    addMark(_mark) {
      const mark = Object.assign(_mark, {
        dir: this.currentDir,
      });

      this.marks.push(mark);
      this.history.add({
        undo: () => {
          this.marks.pop()
        },
        redo: () => {
          this.marks.push(mark);
        },
      });
    },

    // 2点間のサブノードを算出して返す
    path(startX, startY, endX, endY) {
      const width = Number(endX) - Number(startX);
      const height = Number(endY) - Number(startY);
      const hypotenuse = Math.sqrt(width ** 2 + height ** 2);

      const unitX = 0.1 * width / hypotenuse;
      const unitY = 0.1 * height / hypotenuse;

      let subNodes = [];
      let diffX = unitX;
      let diffY = unitY;

      while(Math.abs(diffX) < Math.abs(width) || Math.abs(diffY) < Math.abs(height)) {
        subNodes.push({
          id: this.generateId(),
          x: String(Number(startX) + diffX),
          y: String(Number(startY) + diffY),
        });
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
      this.initialize();
    },

    start() {
      // routes が空のときはアニメーションできない
      if (this.routes.length <= 0) {
        return;
      }

      this.animate = true;
      this.animateIndex = 0;

      clearTimeout(this.animateTimer);
      this.animateTimer = setTimeout(this.next, 1000);
    },

    next() {
      this.animateIndex++;
      if (this.routes.length < this.animateIndex + 1) {
        this.stop();
        return;
      }

      this.animateTimer = setTimeout(this.next, this.routes[this.animateIndex].isMain ? 1000 : 100);
    },

    stop() {
      clearInterval(this.animateTimer);
      this.animate = false;
      this.animateIndex = null;
    },

    up(liftHeight) {
      // 選択したポイントが1つもなければ、荷上げの基準点が算出できない
      if (this.marks.length <= 0) {
        return;
      }

      let mark = Object.assign({}, this.currentNode);
      mark.lift = true;
      mark.up = liftHeight;
      // TODO:荷上げ荷下げを連続するとそれもコピーしてしまう、参照元を見直した方がいいかも
      delete mark.down;

      this.marks.push(mark);
      this.history.add({
        undo: () => {
          this.marks.pop()
        },
        redo: () => {
          this.marks.push(mark);
        },
      });
    },

    down(liftHeight) {
      // 選択したポイントが1つもなければ、荷上げの基準点が算出できない
      if (this.marks.length <= 0) {
        return;
      }

      let mark = Object.assign({}, this.currentNode);
      mark.lift = true;
      // TODO:荷上げ荷下げを連続するとそれもコピーしてしまう、参照元を見直した方がいいかも
      delete mark.up;
      mark.down = liftHeight;

      this.marks.push(mark);
      this.history.add({
        undo: () => {
          this.marks.pop()
        },
        redo: () => {
          this.marks.push(mark);
        },
      });
    },
  },
}
</script>

<style scoped>
.log {
  max-height: 300px;
  overflow: scroll;
  padding: 0.5rem;
  background: #eee;
}

.log p {
  line-height: 1.1;
}
</style>
