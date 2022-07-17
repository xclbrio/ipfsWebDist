
<template>
  <div id="app">
    
    <router-view></router-view>

  </div>
</template>

<script>

  import 'normalize.css';
  import headerMain from './components/header.vue'
  import web3 from './services/connectWeb3'
  import exchange from './exchange.js'
  import settings from './settings.json'

  export default {
    name: 'app',
    components: {
      headerMain,
    },
    data: function () {
      return {
        from: '',
      }
    },
    computed: {
      contract() {
        return exchange.initContract(web3, settings.exchangeAbi, settings.contractAddress);
      }
    },
    created () {
      console.log(web3)
    }
    
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
