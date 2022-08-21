import Vue from "vue";
import Vuex from "vuex";
import web3 from "../services/connectWeb3";
import VuexPersistence from "vuex-persist";
import { pairs } from "../settings.json";
import router from "../router";

Vue.use(Vuex);

const vuexLocal = new VuexPersistence({
  storage: window.localStorage,
});

export default new Vuex.Store({
  state() {
    return {
      currentAccount: null,
      balance: [0, 0],
      gasPrice: 0,
      walletType: "",
      accounts: [],
      privateKey: "",
      pairs,
    };
  },

  getters: {
    isMetamaskConnected(state) {
      return (state.currentAccount && state.currentAccount.metamask) || false;
    },
    metamaskAccount(state) {
      return state.accounts.find((account) => account.metamask) || null;
    },
    localAccounts(state) {
      return state.accounts.filter((el) => !el.metamask);
    },
    currentPair(state) {
      return state.pairs.find(
        (pair) => pair.path === router.currentRoute.params.id
      );
    },
  },

  mutations: {
    setAccounts(state, payload) {
      state.accounts = payload;
    },
    setCurrentAccount(state, payload) {
      state.currentAccount = payload;
    },
    addAccount(state, payload) {
      state.accounts.push(payload);
    },
    deleteAccount(state, payload) {
      state.accounts = state.accounts.filter(
        (account) => account.address !== payload.address
      );
    },
  },

  actions: {
    async getAccounts({ state, commit }) {
      const accounts = await web3.eth.getAccounts().then((res) =>
        res.map((address) => ({
          metamask: true,
          address,
        }))
      );

      commit(
        "setAccounts",
        state.accounts.filter(({ metamask }) => !metamask).concat(accounts)
      );

      if (!state.currentAccount || state.currentAccount.metamask) {
        commit("setCurrentAccount", accounts[0]);
      }
    },
    async createAccount({ commit }) {
      const account = await web3.eth.accounts.create();
      commit("addAccount", account);
      commit("setCurrentAccount", account);
    },
    importAccount({ store, commit }, pk) {
      const account = web3.eth.account.privateKeyToAccount(pk);
      if (!store.accounts.includes(account)) {
        commit("addAccount", account);
        commit("setCurrentAccount", account);
      }
    },
  },

  plugins: [vuexLocal.plugin],
});
