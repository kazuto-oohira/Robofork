<template>
  <router-view></router-view>
</template>

<script>
export default {
  name: 'app',

  props: [
    'saveCallback',
    'cancelCallback',
    'updateCallback',
  ],
}

// TODO: 共通部分がどれなのか判断してから PageOperationPlanDetail からこちらに移動
</script>
