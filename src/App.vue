<template>
  <div class="app">
    <main>
      <!-- All routes will be displayed in here -->
      <router-view/>
    </main>
  </div>
</template>

<script>

export default {
  name: 'App',
};

</script>

<style lang="scss">
@import "./assets/scss/base.scss";
</style>

<style lang="scss" scoped>
//Styles scoped for App.vue
.app{
  display: block;
  width: 100%;
}
</style>
