<template>
  <div class="container-fluid" id="command-viewer">
    <div class="row table-container pre-scrollable">
      <table class="table table-striped">
        <thead>
          <tr>
            <th>No</th>
            <th>Task</th>
            <th>Speed</th>
            <th>Angle</th>
            <th>Lift</th>
            <th>Stop</th>
            <th>X</th>
            <th>Y</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(node, index) in routes" v-if="showAll || isMainNode(node)">
            <th scope="row">{{ index + 1 }}</th>
            <td>{{ task[index] }}</td>
            <td>1000</td>
            <td>0</td>
            <td>{{ height[index] }}</td>
            <td>{{ flagStop[index] }}</td>
            <td>{{ node.x | rounded }}</td>
            <td>{{ node.y | rounded }}</td>
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

  computed: {
    task() {
      return this.routes.map(item => {
        // if (item.isMain && item.up !== null) {
        //   return '荷上げ';
        // }
        // if (item.isMain && item.down !== null) {
        //   return '荷下げ';
        // }

        return item.dir === 0 ? '前進' : 'バック';
      });
    },

    height() {
      return this.routes.map(item => {
        if (!item.isMain) {
          return 0;
        }
        // if (item.up !== null) {
        //   return item.up;
        // }
        // if (item.down !== null) {
        //   return item.down;
        // }

        return 0;
      });
    },

    flagStop() {
      return this.routes.map(item => {
        return 0;
      });
    }
  },

  methods: {
    isMainNode: function(node) {
      return !!node.isMain;
    },
  },

  filters: {
    rounded(point) {
      return String(point).substr(0, 7);
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
