<template>
  <div class="home">
    <img class="img-responsive center-block" src="/static/robofork_app/img/test/map1.png" alt="dummy" width="502" height="394">
  </div>
</template>

<script>
export default {
  name: 'home',

  data () {
    return {
      locationId: this.$route.params.locationId,
    }
  },
}
</script>
