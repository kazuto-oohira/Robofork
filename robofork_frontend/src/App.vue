<template>
  <div class="operation-plan-detail">
    <div class="row">
      <div class="col-md-6">
        <h2>マップ画面</h2>
        <map-viewer
          :width="config.imageWidth"
          :height="config.imageHeight"
          :scaleX="Number(config.scaleX)"
          :scaleY="Number(config.scaleY)"
          :offsetX="Number(config.offsetX)"
          :offsetY="Number(config.offsetY)"
          :imageUrl="config.imageUrl"
          :commands="commands"
          :mainNodes="mainNodes"
          :subNodes="subNodes"
          :animate="animate"
          :animateIndex="animateIndex"
          :selectedCommandIndex.sync="selectedCommandIndex"
          @addMark="addMark"
        ></map-viewer>
      </div>
      <div class="col-md-6">
        <h2>指示画面</h2>
        <command-viewer
          :commands="commands"
          :animate="animate"
          :selectedCommandIndex.sync="selectedCommandIndex"
          @removeMark="removeMark"
        ></command-viewer>
      </div>
    </div>
    <div class="row">
      <div class="col-md-6">
        <terminal
          :hasCommands="this.commands.length > 0"
          :animate="animate"
          :currentDir.sync="currentDir"
          @clear="clear"
          @start="start"
          @stop="stop"
          @save="save"
        ></terminal>

        <div class="log">
          <p>animate: {{ animate }}</p>
          <p>animateIndex: {{ animateIndex }}</p>
          <p>marks: {{ marks }}</p>
          <p>mainNodes: {{ mainNodes }}</p>
          <p>commands: {{ commands }}</p>
          <p>selectedCommandIndex: {{ selectedCommandIndex }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Vue from 'vue'
import axios from 'axios'

import * as Constants from './Constants'
import MapViewer from './MapViewer'
import CommandViewer from './CommandViewer'
import Terminal from './Terminal'

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
      animate: false,
      animateIndex: 0,
      currentDir: true,
      selectedCommandIndex: 0,
    }
  },

  computed: {
    mainNodes() {
      // marks から自動算出する
      if (this.marks.length <= 0) {
        return [];
      }

      this.nodeIndex = Constants.START_NODE_INDEX;

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
            item.task = current.task;
            item.afterTask = Constants.TASK_NOTHING;

            return item;
          }),
        });
        return current;
      });

      return nodes;
    },

    currentId() {
      if (this.mainNodes.length <= 0) {
        return null;
      }
      return this.mainNodes[this.mainNodes.length - 1].id;
    },

    commands() {
      // mainNodes, subNodes から自動算出する
      const startNode = this.mainNodes.find(item => item.id === Constants.START_NODE_INDEX);
      if (!startNode) {
        return [];
      }

      let nodes = [startNode];

      this.mainNodes.reduce((prev, current) => {
        // subNodes の中から path プロパティ内に両端のノードを含むものを探す
        const subNode = this.subNodes.find(item => item.path.includes(current.id) && item.path.includes(prev.id));
        if (!subNode) {
          console.error(`subNode is not found: path = ${[prev, current]}`);
        }

        // subNode
        nodes.push(...subNode.nodes);

        // mainNode
        nodes.push(current);

        return current;
      });

      return nodes;
    },
  },

  created() {
    const loadConfigPromise = axios.get(Constants.CONFIG_ENDPOINT);
    const loadCommandsPromise = axios.get(Constants.LOAD_ENDPOINT);

    loadConfigPromise
      .then(response => {
        const config = response.data;

        if ('config' in config) {
          this.config = config.config;
          this.currentDir = ('startDir' in this.config) && Number(this.config.startDir) === 1;
        } else {
          throw new Error('not exist config');
        }

        return loadCommandsPromise;
      })
      .then(response => {
        const commands = response.data;

        if ('commands' in commands) {
          this.marks = commands.commands.filter(item => item.isMain);
          this.selectedCommandIndex = this.marks.length - 1;
        }

        if (this.marks.length <= 0) {
          this.initialize();
        }
      })
      .catch(error => {
        console.error(error);

        if (this.marks.length <= 0) {
          this.initialize();
        }

        return;
      });
  },

  methods: {
    initialize() {
      this.animate = false;
      this.marks = [];

      if ('startX' in this.config && 'startY' in this.config) {
        this.addMark({
          x: this.config.startX,
          y: this.config.startY,
          task: Constants.TASK_NOTHING,
          afterTask: Constants.TASK_NOTHING,
        });
      }
    },

    generateId() {
      return this.nodeIndex++;
    },

    addMark(_mark) {
      const mark = Object.assign(_mark, {
        task: (() => {
          if (this.marks.length <= 0) {
            return Constants.TASK_NOTHING;
          }
          return this.currentDir ? Constants.TASK_REVERSE : Constants.TASK_FORWARD;
        })(),
        afterTask: Constants.TASK_NOTHING,
        speed: Constants.INITIAL_SPEED,
        angle: Constants.INITIAL_ANGLE,
      });

      this.marks.push(mark);
      this.selectedCommandIndex = this.marks.length - 1;
    },

    removeMark(id) {
      this.marks.splice(id, 1);
      // DOM の更新終わってから
      Vue.nextTick(() => {
        this.selectedCommandIndex = this.marks.length - 1;
      })
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

    clear() {
      this.initialize();
    },

    start() {
      // commands が空のときはアニメーションできない
      if (this.commands.length <= 0) {
        return;
      }

      this.animate = true;
      this.animateIndex = 0;

      clearTimeout(this.animateTimer);
      this.animateTimer = setTimeout(this.next, 10 * Constants.ANIMATION_SPEED);
    },

    next() {
      this.animateIndex++;
      if (this.commands.length < this.animateIndex + 1) {
        this.stop();
        return;
      }

      const nextDuration = Constants.ANIMATION_SPEED * (this.commands[this.animateIndex].isMain ? 10 : 1);
      this.animateTimer = setTimeout(this.next, nextDuration);
    },

    stop() {
      clearInterval(this.animateTimer);
      this.animate = false;
      this.animateIndex = null;
    },

    save() {
      axios({
        method: 'post',
        url: Constants.SAVE_ENDPOINT,
        data: {
          commands: this.commands,
        },
      })
      .then(() => {
        alert('保存しました');
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
