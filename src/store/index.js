import Vue from 'vue'
import Vuex from 'vuex'
import web3 from '../services/connectWeb3'

Vue.use(Vuex)

export default new Vuex.Store({
    state () {
        return {
            currentAccount: '',
            balance: [0, 0],
            gasPrice: 0,
            walletType: '',
            accounts: [],
            privateKey: '',
        }
        
    },

    mutations: {
        setAccounts (state, payload) {
            state.accounts = payload
        },
        setCurrentAccount (state, payload) {
            state.currentAccount = payload
        }
    },

    actions: {
        async getAccounts ({ state, commit }) {
            const accounts = await web3.eth.getAccounts()
            commit('setAccounts', accounts)
            if (!state.currentAccount) commit('setCurrentAccount', accounts[0])
        }
    }
})