<template>
  <div class="container-fluid" id="command-viewer">
    <div class="row table-container pre-scrollable">
      <table class="table table-hover">
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
            <th>Delete</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(command, index) in commands"
            v-if="enableCommand[index]"
            :class="{ 'active': isSelectedCommand(command.id) }"
            @click="selectColumn(command.id)"
          >
            <th scope="row">{{ index + 1 }}</th>
            <td>{{ command.task | taskLabel }}</td>
            <td>{{ command.afterTask | afterTaskLabel }}</td>
            <td>1000</td>
            <td>0</td>
            <td>{{ liftHeight[index] }}</td>
            <td>{{ flagStop[index] }}</td>
            <td>{{ command.x | rounded }}</td>
            <td>{{ command.y | rounded }}</td>
            <td>
              <button
                class="btn btn-warning"
                type="button"
                v-if="command.isMain && command.id !== 0"
                @click="remove(command.id)"
              >delete</button>
            </td>
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
import * as Constants from './Constants'

export default {
  name: 'command-viewer',

  props: [
    'commands',
    'selectedCommandIndex',
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

    liftHeight() {
      return this.commands.map(item => {
        if ('up' in item) {
          return item.up;
        }
        if ('down' in item) {
          return item.down;
        }

        return 0;
      });
    },

    flagStop() {
      return this.commands.map((item, index) => item.afterTask !== Constants.TASK_NOTHING ? 1 : 0);
    }
  },

  methods: {
    isMainNode(node) {
      return !!node.isMain;
    },

    isSelectedCommand(id) {
      return id === this.selectedCommandIndex;
    },

    selectColumn(id) {
      this.$emit('update:selectedCommandIndex', id);
    },

    remove(id) {
      this.$emit('removeMark', id);
    },
  },

  filters: {
    rounded(point) {
      return String(point).substr(0, 7);
    },

    taskLabel(taskIndex) {
      return Constants.TASK_LABELS[taskIndex];
    },

    afterTaskLabel(taskIndex) {
      if (taskIndex === Constants.TASK_NOTHING) {
        return '-';
      }

      return Constants.TASK_LABELS[taskIndex];
    },
  },
}
</script>

<style scoped>
.table-container {
  min-height: 350px;
  border: 1px solid #333;
}

tr {
  cursor: pointer;
}
</style>
