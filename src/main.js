import Vue from 'vue'
import VueResource from 'vue-resource'
import VueRouter from 'vue-router'
import App from './App.vue'
import settings from './settings.json'
import VueSocketio from 'vue-socket.io'
import Highcharts from 'highcharts'
import stockInit from 'highcharts/modules/stock'
import store from './store'
import router from './router'

Vue.use(new VueSocketio({
    debug: true,
    connection: settings.wsURL
}))
Vue.use(VueResource)
Vue.use(VueRouter)
Vue.use(store)

stockInit(Highcharts)

Number.prototype.noExponents = function() {
  var data = String(this).split(/[eE]/);
  if (data.length == 1) return data[0];

  var z = '',
    sign = this < 0 ? '-' : '',
    str = data[0].replace('.', ''),
    mag = Number(data[1]) + 1;

  if (mag < 0) {
    z = sign + '0.';
    while (mag++) z += '0';
    return z + str.replace(/^\-/, '');
  }
  mag -= str.length;
  while (mag--) z += '0';
  return str + z;
}

if (window.innerWidth < 800) {
  let curLocation = location.href;
  let mobLocation = curLocation.slice(0, curLocation.indexOf('e')) + "m." + curLocation.slice(curLocation.indexOf('e'));

  location.replace(`${mobLocation}`)
}


new Vue({
  render: h => h(App),
  router,
  store,
}).$mount('#app')