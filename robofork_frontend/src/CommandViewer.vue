<template>
  <div id="command-viewer">
    <div class="row table-container pre-scrollable" ref="scrollContainer">
      <table class="table table-striped jambo_table bulk_action">
        <thead>
          <tr>
            <!--<th>No</th>-->
            <th>Task</th>
            <th>AfterTask</th>
            <th>Speed</th>
            <th>Lift</th>
            <th>X</th>
            <th>Y</th>
            <th>Delete</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(command, index) in commands"
            v-if="enableCommand[index]"
            ref="commandsElements"
            :value="$el"
            :class="{ 'active': isSelectedCommand(command.id) }"
            @click="selectColumn(command.id)"
          >
            <!--<td scope="row">{{ index + 1 }}</td>-->
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
            <td>
              <span v-if="!isSelectedCommand(command.id)">{{ command.speed }}</span>
              <input class="form-control speed" v-if="isSelectedCommand(command.id)" v-model="command.speed">
            </td>
            <td>
              <span v-if="!isSelectedCommand(command.id)">{{ liftHeight[index] }}</span>
              <input class="form-control lift-height" v-if="isSelectedCommand(command.id)" v-model="command.liftHeight">
            </td>
            <td>
              <span v-if="!isSelectedCommand(command.id)">{{ command.x }}</span>
              <input class="form-control coordinate" v-if="isSelectedCommand(command.id)" v-model="command.x">
            </td>
            <td>
              <span v-if="!isSelectedCommand(command.id)">{{ command.y }}</span>
              <input class="form-control coordinate" v-if="isSelectedCommand(command.id)" v-model="command.y">
            </td>
            <td>
              <button
                class="btn btn-danger btn-xs"
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
    <!--
    <div class="row">
      <div class="checkbox">
        <label>
          <input type="checkbox" v-model="checkSubNodes"> サブノードも含めて表示する
        </label>
      </div>
    </div>
    -->
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

  data() {
    return {
      checkSubNodes: false,
      afterTaskChoices: [
        { index: Constants.TASK_NOTHING,  label: Constants.TASK_LABELS[Constants.TASK_NOTHING] },
        { index: Constants.TASK_LIFTUP,   label: Constants.TASK_LABELS[Constants.TASK_LIFTUP] },
        { index: Constants.TASK_LIFTDOWN, label: Constants.TASK_LABELS[Constants.TASK_LIFTDOWN] },
        { index: Constants.TASK_PAUSE, label: Constants.TASK_LABELS[Constants.TASK_PAUSE] },
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
  },

  updated() {
    this.focusSelectedCommand();
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

    focusSelectedCommand() {
      if (!('commandsElements' in this.$refs) || !('scrollContainer' in this.$refs)) {
        return;
      }

      const container = this.$refs.scrollContainer;
      const el = this.$refs.commandsElements[this.selectedCommandIndex];

      if (!el) {
        return;
      }

      let offsetTop = 0;
      if (this.selectedCommandIndex >= 1) {
        offsetTop = el.offsetTop;
      }

      container.scrollTop = offsetTop;
    },
  },

  filters: {
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
  box-sizing: border-box;
  padding: 1px;
  border: 1px solid #ccccc;
}

.table th,
.table td {
  border-top: 0;
  vertical-align: middle;
}

.table tr {
}

.after-task {
  width: 10rem;
}

.lift-height {
  width: 5rem;
}
</style>
