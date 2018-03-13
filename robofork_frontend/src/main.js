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

new Vue({
  el: '#app',
  render: h => h(App),
  router,
});
