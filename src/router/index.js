import Vue from 'vue';
import VueRouter from 'vue-router';
import VidispineVersion from '../components/VidispineVersion.vue';
import Import from '../components/Import.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'import',
    component: Import,
  },
  {
    path: '/version',
    name: 'version',
    component: VidispineVersion,
  },
];

export default new VueRouter({
  routes,
  mode: 'history',
});
