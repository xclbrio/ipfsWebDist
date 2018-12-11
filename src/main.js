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

stockInit(Highcharts)

Vue.use(HighchartsVue)



Vue.use(VueSocketio, settings.wsURL);
Vue.use(VueResource)
Vue.use(VueTabs)
Vue.use(VueRouter)


// Vue.config.productionTip = false

// var web3 = new Web3(new Web3.providers.HttpProvider("https://kovan.infura.io/GiDCavBXupdlU3zX2SVo"));

// console.log(web3)

Number.prototype.noExponents = function(){
    var data = String(this).split(/[eE]/);
    if(data.length == 1) return data[0]; 

    var  z = '', 
    sign = this < 0 ? '-' : '',
    str = data[0].replace('.', ''),
    mag = Number(data[1]) + 1;

    if(mag < 0){
        z = sign + '0.';
        while(mag++) z + = '0';
        return z + str.replace(/^\-/,'');
    }
    mag -= str.length;  
    while(mag--) z += '0';
    return str + z;
}

if (window.innerWidth < 800) {
  var token = location.search;
  var hash = location.hash;

  let curLocation = location.href;
  let mobLocation = curLocation.slice(0, curLocation.indexOf('x')) + "m." + curLocation.slice(curLocation.indexOf('x'));

  location.replace(`${mobLocation}`)
}

var router = new VueRouter({
  routes: [
  	{path: '/:id', name: 'pair', component: workflow},
  	{path: '', redirect: settings.pairs[0].path},
  ]
})

var app = new Vue({
	render: h => h(App),
	router: router,	

}).$mount('#app')

