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
            <td>
              <span v-if="!isSelectedCommand(command.id)">{{ command.afterTask | afterTaskLabel }}</span>
              <select
                class="form-control after-task"
                v-if="isSelectedCommand(command.id)"
                v-model="command.afterTask"
              >
                <option v-for="choice in afterTaskChoices" :value="choice.index">{{ choice.label }}</option>
              </select>
            </td>
            <td>1000</td>
            <td>0</td>
            <td>
              <span v-if="!isSelectedCommand(command.id)">{{ liftHeight[index] }}</span>
              <input class="form-control lift-height" v-if="isSelectedCommand(command.id)" v-model="command.liftHeight">
            </td>
            <td>{{ flagStop[index] }}</td>
            <td>{{ command.x | rounded }}</td>
            <td>{{ command.y | rounded }}</td>
            <td>
              <button
                class="btn btn-warning"
                type="button"
                v-if="command.isMain && command.id !== 0"
                :disabled="disableRemove"
                @click="remove(command.id)"
              >ノード削除</button>
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
    'animate',
    'selectedCommandIndex',
  ],

  data () {
    return {
      checkSubNodes: false,
      afterTaskChoices: [
        { index: Constants.TASK_NOTHING,  label: Constants.TASK_LABELS[Constants.TASK_NOTHING] },
        { index: Constants.TASK_LIFTUP,   label: Constants.TASK_LABELS[Constants.TASK_LIFTUP] },
        { index: Constants.TASK_LIFTDOWN, label: Constants.TASK_LABELS[Constants.TASK_LIFTDOWN] },
      ],
    }
  },

  computed: {
    enableCommand() {
      return this.commands.map(item => {
        return this.checkSubNodes || this.isMainNode(item);
      });
    },

    disableRemove() {
      return this.animate;
    },

    liftHeight() {
      return this.commands.map(item => {
        if ('afterTask' in item && (item.afterTask === Constants.TASK_LIFTUP || item.afterTask === Constants.TASK_LIFTDOWN)) {
          return item.liftHeight;
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
      if (this.selectedCommandIndex === 0) {
        return false;
      }

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

.table th,
.table td {
  border-top: 0;
  vertical-align: middle;
}

.table tr {
  height: 6rem;
}

.after-task {
  width: 10rem;
}

.lift-height {
  width: 5rem;
}
</style>
