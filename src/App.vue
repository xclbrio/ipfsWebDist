
<template>
  <div id="app">
    
    <router-view></router-view>

  </div>
</template>

<script>

  import 'normalize.css';

  export default {
    name: 'app',
  }

</script>

<style lang="scss">
  @import url('https://fonts.googleapis.com/css?family=Roboto+Mono:400,700');
  @import '_base.scss';
  body{
    background-color: $black;
    max-width: 100vw;
    overflow-x: hidden;
  }
  #app {
    font-family: 'Roboto Mono', monospace;
    font-weight: 700;
    height: 100vh;
    width: 100vw !important;
    overflow-x: hidden;

  }


</style>
