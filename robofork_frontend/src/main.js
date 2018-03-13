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
      path: '/:location_id',
      component: PageHome,
    },
    {
      path: '/:location_id/operation_plan/:vehicle_operation_plan_id',
      component: PageOperationPlanDetail,
    },
  ],
});

new Vue({
  el: '#app',
  render: h => h(App),
  router,
});
