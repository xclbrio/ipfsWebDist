
<template>
  <div id="app">
    
    <router-view></router-view>

  </div>
</template>

<script>

  import 'normalize.css';
  import headerMain from './components/header.vue'
  import exchange from './exchange.js'
  import settings from './settings.json'


  export default {
    name: 'app',
    data: function () {
      return {
        from: '',
        contract: '',
      }
    },
    components: {
      headerMain,
    },
    methods: {
      
    },
    created(){
      var vm = this;

      try {
        this.contract = exchange.initContract(web3, settings.exchangeAbi, settings.contractAddress);
      } catch(e) {
        console.log(e);
      }

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
