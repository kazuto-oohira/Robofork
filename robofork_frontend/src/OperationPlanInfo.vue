<template>
  <div class="container-fluid" id="operation-plan-info">
  </div>
</template>

<script>
import * as Constants from './Constants'

export default {
  name: 'operation-plan-info',

  props: [
    // 'hasCommands',
    // 'animate',
    // 'currentDir',
  ],

  data() {
    return {
    }
  },

  computed: {
    // dirLabel() {
    //   if (!this.hasCommands) {
    //     return '-';
    //   }
    //
    //   return this.currentDir ? Constants.DIR_FORWARD : Constants.DIR_REVERSE;
    // },
  },

  methods: {
    // reverse() {
    //   this.$emit('reverse');
    // },
    //
    // save() {
    //   this.$emit('save');
    // },
  },
}
</script>

<style scoped>
/*.checkbox label {*/
  /*user-select: none;*/
/*}*/

/*.row {*/
  /*margin-bottom: 1rem;*/
/*}*/
</style>
