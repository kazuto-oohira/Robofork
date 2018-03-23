<template>
  <div class="operation-plan-detail">
    <div class="row">
      <div class="col-md-12">
        <operation-plan-info
          :planInfo="this.planInfo"
          @changeValue="changePlanInfoValue"
        ></operation-plan-info>
      </div>
    </div>
    <div class="row">
      <div class="col-md-12">
        <div class="x_panel">
          <div class="x_title">
            <h2>運行計画マップ</h2>
            <div class="clearfix"></div>
          </div>
          <div class="x_content">
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
              :hasCommands="this.commands.length > 0"
              :currentDir="currentDir"
              @addMark="addMark"
              @updateMark="updateMark"
              @clear="clear"
              @start="start"
              @stop="stop"
              @reverse="reverse"
            ></map-viewer>
          </div>
        </div>
      </div>
      <div class="col-md-12">
        <div class="x_panel">
          <div class="x_title">
            <h2>運行計画一覧</h2>
            <div class="clearfix"></div>
          </div>
          <div class="x_content">
            <command-viewer
              :commands="commands"
              :animate="animate"
              :selectedCommandIndex.sync="selectedCommandIndex"
              @removeMark="removeMark"
            ></command-viewer>
          </div>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="col-md-12">
        <button @click="back()" class="btn btn-default pull-left">キャンセル/戻る</button>
        <button @click="save()" class="btn btn-success btn-lg pull-right">ルートを保存する</button>
      </div>
      <div class="clearfix">&nbsp;</div>
    </div>
  </div>
</template>

<script>
import Vue from 'vue'
import axios from 'axios'

import * as Constants from './Constants'
import MapViewer from './MapViewer'
import CommandViewer from './CommandViewer'
import OperationPlanInfo from "./OperationPlanInfo";

export default {
  name: 'page-operation-plan-detail',

  components: {
    'operation-plan-info': OperationPlanInfo,
    'map-viewer': MapViewer,
    'command-viewer': CommandViewer,
  },

  data () {
    return {
      locationId: this.$route.params.locationId,
      vehicleOperationPlanId: this.$route.params.vehicleOperationPlanId,

      config: {},
      marks: [],
      animate: false,
      animateIndex: 0,
      currentDir: true,
      selectedCommandIndex: 0,

      planInfo: {
        name: '',
        explain: '',
        priority: -1,
        vehicle: {}
      },
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
        nodes.push(...subNode.nodes.map(item => Object.assign(item, { stop: 0 })));

        // mainNode
        nodes.push(Object.assign(current, {
          stop: current.afterTask !== Constants.TASK_NOTHING ? 1 : 0,
        }));

        return current;
      });

      return nodes;
    },
  },

  created() {
    const loadConfigPromise = axios.get(Constants.CONFIG_ENDPOINT(this.locationId));
    const loadCommandsPromise = axios.get(Constants.LOAD_ENDPOINT(this.vehicleOperationPlanId));

    loadConfigPromise
      .then(response => {
        const config = response.data;

        if ('config' in config) {
          this.config = config.config;
          this.currentDir = this.config.startDirection === 0;
        } else {
          throw new Error('not exist config');
        }

        // 新規作成時はloadCommandsPromiseが失敗するので
        this.planInfo = {
          vehicles: this.config.vehicles,
        }

        return loadCommandsPromise;
      })
      .then(response => {
        const commands = response.data;

        if (('commands' in commands) && Array.isArray(commands.commands)) {
          this.marks = commands.commands.filter(item => item.isMain);
          this.selectedCommandIndex = this.marks.length - 1;
        }

        if (this.marks.length <= 0) {
          this.initialize();
        }

        this.planInfo = {
          name: commands.name || "",
          explain: commands.explain || "",
          priority: commands.priority || 0,
          vehicle: commands.vehicle,
          vehicles: this.config.vehicles,
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
      _mark["x"] = this.rounded(_mark["x"]);
      _mark["y"] = this.rounded(_mark["y"]);
      const mark = Object.assign(_mark, {
        task: (() => {
          if (this.marks.length <= 0) {
            return Constants.TASK_NOTHING;
          }
          return this.currentDir ? Constants.TASK_FORWARD : Constants.TASK_REVERSE;
        })(),
        afterTask: Constants.TASK_NOTHING,
        speed: Constants.INITIAL_SPEED,
        angle: Constants.INITIAL_ANGLE,
      });

      this.marks.push(mark);
      this.selectedCommandIndex = this.marks.length - 1;
    },

    updateMark(id, _mark) {
      Vue.set(this.marks[id], 'x', this.rounded(_mark.x));
      Vue.set(this.marks[id], 'y', this.rounded(_mark.y));
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
          x: String(this.rounded(Number(startX) + diffX)),
          y: String(this.rounded(Number(startY) + diffY)),
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

    reverse() {
      this.currentDir = !this.currentDir;

      if (this.marks.length <= 1) {
        return;
      }

      const currentMark = this.marks[this.marks.length - 1];
      Vue.set(currentMark, 'task', currentMark.task === Constants.TASK_FORWARD ? Constants.TASK_REVERSE : Constants.TASK_FORWARD);
    },

    changePlanInfoValue(value) {
      for (const key in value) {
        this.planInfo[key] = value[key];
      }
    },

    save() {
      axios({
        method: 'post',
        url: Constants.SAVE_ENDPOINT(this.vehicleOperationPlanId),
        data: {
          location_id: this.locationId,
          commands: this.commands,
          planInfo: this.planInfo,
        },
      })
      .then(() => {
        // jQuery使っちゃってごめんなさい...
        $(document).trigger('showInfoAlert', { message: '保存しました' });
      });
    },

    back() {
      window.location = Constants.PREV_PAGE_URL(this.locationId);
    },

    rounded(point) {
      let result = "0.00";
      if (!isNaN(point)) {
        result = String(Math.round(parseFloat(point) * 100) / 100);
      }
      return result;
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
