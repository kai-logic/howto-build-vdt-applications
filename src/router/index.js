import Vue from 'vue';
import VueRouter from 'vue-router';
import VidispineVersion from '../components/VidispineVersion.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'version',
    component: VidispineVersion,
  },
];

export default new VueRouter({
  routes,
  mode: 'history',
});
