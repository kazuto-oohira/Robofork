<template>
  <div class="container-fluid" id="command-viewer">
    <div class="row table-container pre-scrollable">
      <table class="table table-striped">
        <thead>
          <tr>
            <th>No</th>
            <th>Task</th>
            <th>AfterTask</th>
            <th>Speed</th>
            <th>Angle</th>
            <th>Lift</th>
            <th>Stop</th>
            <th>X</th>
            <th>Y</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(node, index) in commands"
            v-if="enableCommand[index]"
          >
            <th scope="row">{{ commandIndex[index] }}</th>
            <td>{{ taskIndex[index] | taskLabel }}</td>
            <td>{{ afterTaskIndex[index] | taskLabel }}</td>
            <td>1000</td>
            <td>0</td>
            <td>{{ liftHeight[index] }}</td>
            <td>{{ node.lift ? '1' : '0' }}</td>
            <td>{{ node.x | rounded }}</td>
            <td>{{ node.y | rounded }}</td>
          </tr>
        </tbody>
      </table>
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
const TASK_LABELS = {
  0: '前進',
  1: 'バック',
  2: '旋回（回転）',
  3: '荷上げ(旋回なし)',
  4: '荷上げ(旋回あり)',
  5: '荷下げ(旋回なし)',
  6: '荷下げ(旋回あり)',
  255: 'なにもしない',
};

export default {
  name: 'command-viewer',

  props: [
    'commands',
  ],

  data () {
    return {
      checkSubNodes: false,
    }
  },

  computed: {
    enableCommand() {
      return this.commands.map(item => {
        return this.checkSubNodes || this.isMainNode(item);
      });
    },

    commandIndex() {
      let commandIndex = 1;

      return this.commands.map((item, index) => {
        if (index >= this.commands.length - 1) {
          return commandIndex++;
        }

        const next = this.commands[index + 1];

        if (next.lift) {
          return commandIndex;
        }

        return commandIndex++;
      });
    },

    taskIndex() {
      return this.commands.map((item, index) => {
        if (index === 0) {
          return 255;
        }
        if (item.lift && 'up' in item) {
          return 3;
        } else if (item.lift && 'down' in item) {
          return 5;
        }

        return item.dir === 0 ? 0 : 1;
      });
    },

    afterTaskIndex() {
      return this.commands.map((item, index) => {
        if (index === 0) {
          return 255;
        }
        if (item.lift && 'up' in item) {
          return 3;
        } else if (item.lift && 'down' in item) {
          return 5;
        }

        return item.dir === 0 ? 0 : 1;
      });
    },

    liftHeight() {
      return this.commands.map(item => {
        if (!item.lift) {
          return 0;
        }
        if ('up' in item) {
          return item.up;
        } else if ('down' in item) {
          return item.down;
        }

        return 0;
      });
    },

    flagStop() {
      return this.commands.map((item, index) => {
        if (index >= this.commands.length - 1) {
          return 0;
        }

        return item.lift ? 1 : 0;
      });
    }
  },

  methods: {
    isMainNode(node) {
      return !!node.isMain;
    },
  },

  filters: {
    rounded(point) {
      return String(point).substr(0, 7);
    },

    taskLabel(taskIndex) {
      return TASK_LABELS[taskIndex];
    },
  },
}
</script>

<style scoped>
.table-container {
  min-height: 350px;
  border: 1px solid #333;
}
</style>
