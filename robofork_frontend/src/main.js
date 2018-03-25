import Vue from 'vue'
import VueRouter from 'vue-router'

import App from './App'
import PageHome from './PageHome'
import PageOperationPlanDetail from './PageOperationPlanDetail'

Vue.use(VueRouter);

const router = new VueRouter({
  mode: 'history',
  routes: [
    {
      path: '/:locationId',
      component: PageHome,
    },
    {
      path: '/:locationId/operation_plan/:vehicleOperationPlanId',
      component: PageOperationPlanDetail,
    },
  ],
});

const root = document.getElementById('app');

new Vue({
  el: root,
  render: h => h(App),
  router,
  data() {
    // Vue.js 外との連携のため、 callback 呼ぶ穴を data attr 経由であける
    return {
      saveCallback: root.dataset.save,
      cancelCallback: root.dataset.cancel,
      updateCallback: root.dataset.update,
    }
  },
});
