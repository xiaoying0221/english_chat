import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    navData: '全局的 nav 数据',
  },
  mutations: {
    setNavData(state, newData) {
      state.navData = newData;
    },
  },
  actions: {
    updateNavData({ commit }, newData) {
      commit('setNavData', newData);
    },
  },
  getters: {
    getNavData: (state) => state.navData,
  },
});
