<template>
  <div class="home">
    <h2>Home 画面</h2>
    <p>locationId: {{ locationId }}</p>
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
