import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    langs: [],
    user: {
      id: null,
      credits: {},
      admin: false,
    },
    loggedIn: null,
  },
  mutations: {
    changeLangs(state, langs) {
      state.langs = langs;
    },
    changeUser(state, user) {
      state.user = user;
    },
    changeLoggedIn(state, b) {
      state.loggedIn = b;
    },
  },
  actions: {
    setUser({ commit }, user) {
      commit("changeUser", user);
    },
    setLangs({ commit }, langs) {
      commit("changeLangs", langs);
    },
    setLoggedIn({ commit }, b) {
      commit("changeLoggedIn", b);
    },
  },
  modules: {},
  getters: {
    getLangs: (state) => state.langs,
    getId: (state) => state.user.id,
    getUser: (state) => state.user,
    getLoggedIn: (state) => state.loggedIn,
  },
});
