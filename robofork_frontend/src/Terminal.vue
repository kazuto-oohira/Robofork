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
        <p style="margin-top: 10px">次の進行方向: {{ dirLabel }}</p>
      </div>
      <div class="col-sm-6">
        <div class="input-group">
          <input type="text" :disabled="disableLiftHeight" class="form-control" placeholder="高さ(mm)" v-model="liftHeight">
          <span class="input-group-btn">
            <button @click="up()" :disabled="disableUp" class="btn btn-default" type="button">荷上げ</button>
            <button @click="down()" :disabled="disableDown" class="btn btn-default" type="button">荷下げ</button>
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import * as Constants from './Constants'

export default {
  name: 'terminal',

  props: [
    'hasRoutes',
    'animate',
    'currentDir',
  ],

  data() {
    return {
      liftHeight: null,
    }
  },

  computed: {
    disableClear() {
      return !this.hasRoutes;
    },

    disableStart() {
      return !this.hasRoutes || this.animate;
    },

    disableStop() {
      return !this.hasRoutes || !this.animate;
    },

    disableReverse() {
      return !this.hasRoutes || this.animate;
    },

    disableLiftHeight() {
      return !this.hasRoutes;
    },

    disableUp() {
      return !this.hasRoutes || !this.liftHeight || this.animate;
    },

    disableDown() {
      return !this.hasRoutes || !this.liftHeight || this.animate;
    },

    dirLabel() {
      if (!this.hasRoutes) {
        return '-';
      }

      return this.currentDir ? Constants.DIR_REVERSE : Constants.DIR_FORWARD;
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
      this.$emit('update:currentDir', 1 - this.currentDir);
    },

    up() {
      this.$emit('up', this.liftHeight);
      this.liftHeight = null;
    },

    down() {
      this.$emit('down', this.liftHeight);
      this.liftHeight = null;
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
