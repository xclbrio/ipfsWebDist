import Vue from 'vue'
import VueTabs from 'vue-nav-tabs'
import VueResource from 'vue-resource'
import VueRouter from 'vue-router'
import App from './App.vue'
import settings from './settings.json'
import exchange from './exchange.js'
import workflow from './components/workflow.vue'
import VueSocketio from 'vue-socket.io'
import HighchartsVue from 'highcharts-vue'
import Highcharts from 'highcharts'
import stockInit from 'highcharts/modules/stock'
import Web3 from 'web3'

stockInit(Highcharts)
Vue.use(HighchartsVue)
Vue.use(VueSocketio, settings.wsURL);
Vue.use(VueResource)
Vue.use(VueTabs)
Vue.use(VueRouter)

const router = new VueRouter({
  routes: [
    {path: '/:id', name: 'pair', component: workflow},
    {path: '', redirect: settings.pairs[0].path},
  ]
})


window.addEventListener('load', async () => {
    if (window.ethereum) {
        window.web3 = new Web3(ethereum);
        try {
            await ethereum.enable();
        } catch (error) {
            throw error
        }
    }
    else if (window.web3) {
        window.web3 = new Web3(web3.currentProvider);
    }
    else {
        window.web3 = new Web3(new Web3.providers.WebsocketProvider("wss://infura.io/ws"));
    }


    const app = new Vue({
      render: h => h(App),
      router: router, 

    }).$mount('#app')
});

Number.prototype.noExponents = function(){
    let data = String(this).split(/[eE]/);
    if(data.length == 1) return data[0]; 

    let z = '', 
    sign = this < 0 ? '-' : '',
    str = data[0].replace('.', ''),
    mag = Number(data[1]) + 1;

    if (mag < 0){
        z = sign + '0.';
        while(mag++) z += '0';
        return z + str.replace(/^\-/,'');
    }
    mag -= str.length;  
    while(mag--) z += '0';
    return str + z;
}

if (window.innerWidth < 800) {
  let token = location.search;
  let hash = location.hash;
  let curLocation = location.href;
  let mobLocation = curLocation.slice(0, curLocation.indexOf('x')) + "m." + curLocation.slice(curLocation.indexOf('x'));
  location.replace(`${mobLocation}`)
}





