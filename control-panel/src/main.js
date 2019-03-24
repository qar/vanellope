// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue';
import iView from 'iview';
import '@/assets/reset.css';
import '@/assets/global.scss';
import 'iview/dist/styles/iview.css';
import 'codemirror/lib/codemirror.css';
import 'codemirror/mode/gfm/gfm';
import '@/assets/sass/main.scss';
import $http from '@/utils/http';
import App from '@/components/App/app.vue';
import router from './router';

Vue.config.productionTip = false;

Vue.use(iView);

Vue.prototype.$http = $http;

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: { App },
});
