import Vue from "vue";
import Vuex from "vuex";
import axios from "../plugins/axios";
import consultingrooms from "./consultingroom";
import appointments from "./appointments";
import patients from "./patients";
import services from "./services";
import treatments from "./treatments";
import payments from "./payments";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    token: localStorage.getItem("token") || "",
    id: localStorage.getItem("id") || "",
    snackbar: {
      show: false,
      message: "",
    },
  },
  getters: {
    isAuthenticated: (state) => !!state.token,
  },
  mutations: {
    setToken(state, token) {
      state.token = token;
      localStorage.setItem("token", token);
    },
    setID(state, id) {
      state.id = id;
      localStorage.setItem("id", id);
    },
    clearToken(state) {
      state.token = "";
      localStorage.removeItem("token");
    },
    showSnackbar(state, message) {
      state.snackbar.show = true;
      state.snackbar.message = message;
    },
    hideSnackbar(state) {
      state.snackbar.show = false;
      state.snackbar.message = "";
    },
  },
  actions: {
    ...appointments,
    ...consultingrooms,
    ...patients,
    ...services,
    ...treatments,
    ...payments,
    async login({ commit }, form) {
      try {
        const response = await axios.post("/login", form);
        commit("setID", JSON.parse(response.data.user)[0].pk);
        commit("setToken", response.data.token);
        return response;
      } catch (e) {
        return e;
      }
    },
    logout({ commit }) {
      commit("clearToken");
    },
    showSnackbar({ commit }, message) {
      commit("showSnackbar", message);
      setTimeout(() => {
        commit("hideSnackbar");
      }, 3000);
    },
  },
  modules: {},
});
