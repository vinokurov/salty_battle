import Vue from 'vue';
import App from './App.vue';
import BootstrapVue from 'bootstrap-vue'
import SvgSprite from 'vue-svg-sprite';

Vue.config.productionTip = false;
Vue.use(BootstrapVue)
Vue.use(SvgSprite, {url:''});


new Vue({
  render: h => h(App),
}).$mount('#app');
