<template>
  <div class="container-fluid" id="terminal">
    <div class="row">
      <div class="col-sm-6 btn-group">
        <button @click="clear()":disabled="disableClear" class="btn btn-warning">clear</button>
      </div>
      <div class="col-sm-6 btn-group">
        <button @click="start()" :disabled="disableStart" class="btn btn-primary">Start</button>
        <button @click="stop()" :disabled="disableStop" class="btn btn-danger">Stop</button>
      </div>
    </div>
    <div class="row">
      <div class="col-sm-6">
        <button @click="reverse()" :disabled="disableReverse" class="btn btn-default">向きを反転する</button>
        <p style="margin-top: 10px">今の進行方向: {{ dirLabel }}</p>
      </div>
      <div class="col-sm-6">
        <button @click="save()" class="btn btn-success">ルートを保存する</button>
      </div>
    </div>
  </div>
</template>

<script>
import * as Constants from './Constants'

export default {
  name: 'terminal',

  props: [
    'hasCommands',
    'animate',
    'currentDir',
  ],

  data() {
    return {
    }
  },

  computed: {
    disableClear() {
      return !this.hasCommands;
    },

    disableStart() {
      return !this.hasCommands || this.animate;
    },

    disableStop() {
      return !this.hasCommands || !this.animate;
    },

    disableReverse() {
      return !this.hasCommands || this.animate;
    },

    dirLabel() {
      if (!this.hasCommands) {
        return '-';
      }

      return this.currentDir ? Constants.DIR_FORWARD : Constants.DIR_REVERSE;
    },
  },

  methods: {
    clear() {
      this.$emit('clear');
    },

    start() {
      this.$emit('start');
    },

    stop() {
      this.$emit('stop');
    },

    reverse() {
      this.$emit('reverse');
    },

    save() {
      this.$emit('save');
    },
  },
}
</script>

<style scoped>
.checkbox label {
  user-select: none;
}

.row {
  margin-bottom: 1rem;
}
</style>
