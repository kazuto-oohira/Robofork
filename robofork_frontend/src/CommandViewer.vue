<template>
  <div class="container-fluid">
    <div class="row table-container pre-scrollable">
      <table class="table table-striped">
        <thead>
          <tr>
            <th>No</th>
            <th>Task</th>
            <th>Speed</th>
            <th>Angle</th>
            <th>Lift</th>
            <th>NodeNo</th>
            <th>X</th>
            <th>Y</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(node, index) in routes" v-if="showAll || isMainNode(node)">
            <th scope="row">{{ index + 1 }}</th>
            <td>Move</td>
            <td>1000</td>
            <td>0</td>
            <td>0</td>
            <td>{{ node.id }}</td>
            <td>{{ node.x }}</td>
            <td>{{ node.y }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="row">
      <div class="checkbox">
        <label>
          <input type="checkbox" v-model="showAll"> サブノードも含めて表示する
        </label>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'command-viewer',
  props: [
    'routes',
  ],

  data () {
    return {
      showAll: false,
    }
  },

  methods: {
    isMainNode: function(node) {
      return !!node.isMain;
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
