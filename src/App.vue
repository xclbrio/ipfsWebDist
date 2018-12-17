
<template>
  <div id="app">
    
    <router-view></router-view>

  </div>
</template>

<script>

  import 'normalize.css';
  import headerMain from './components/header.vue'

  import provider from './provider.js'
  import exchange from './exchange.js'
  import settings from './settings.json'

  const web3 = provider.connectWeb3();



  export default {
    name: 'app',
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
    components: {
      headerMain,
    },
    created(){
      var vm = this;

      setInterval(function () {
        try {
          web3.eth.getAccounts().then(res => vm.from = res[0]);
        } catch(e) {
          
        }
        
      }, 5000)
      

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
