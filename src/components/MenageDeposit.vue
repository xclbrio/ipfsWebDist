<template>
  <form @submit.prevent="menageDeposit" class="forms__box form__manage">
    <p class="input__title --greyish">
      {{ isWithdraw ? "WITHDROW" : "DEPOSIT" }} ->
      <span v-for="(item, index) in currentPair.tokens" :key="item">
        <label :class="{ active: item === token }" class="expries">
          <input class="radio-btn" type="radio" :value="item" v-model="token" />
          {{ currentPair.symbols[index] }}
        </label>
      </span>
      [choose currency]
    </p>
    <p class="input__contaner --amount">
      <input
        v-model.number="amount"
        placeholder="amount_"
        type="number"
        step="any"
        required
      />
      <button type="submit" class="btn btn_deposit">SEND</button>
    </p>

    <alert
      ctx="transaction"
      title="TRANSACTION"
      v-if="showTransactionModal"
      @close="showTransactionModal = false"
    >
      <div class="copy-input">
        <div class="container">
          <input
            id="hash"
            v-model="trasnactionData.blockHash"
            type="text"
          /><button @click="copyHash" class="copy">
            <img src="../assets/copy-ico.svg" alt="" />
          </button>
        </div>
        <div class="etherscan">
          <a target="_blank" :href="txlink">VIEW ON ETHERSCAN</a>
        </div>
      </div>
    </alert>

    <alert
      v-if="showWithdorawAlert"
      @close="showWithdorawAlert = false"
      ctx="error"
      title="ATTENTION"
    >
      <p class="withdraw-alert">
        <span>All your orders will be deleted!</span>
        <button @click="withdraw" class="btn accept">Accept</button>
      </p>
    </alert>
  </form>
</template>

<script>
import { mapGetters, mapState } from "vuex";
import exchange from "@/exchange";
import settings from "@/settings.json";
import { convertToWei } from "@/services/helpers";
import Alert from '@/components/Alert';

export default {
  components: {
    Alert
  },
  props: {
    isWithdraw: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      amount: null,
      token: null,
      trasnactionData: null,
      showTransactionModal: false,
      showWithdorawAlert: false,
    };
  },
  computed: {
    isEth() {
      return this.token === "0x0000000000000000000000000000000000000000";
    },
    txlink() {
      return `${settings.network.etherscan}tx/${this.txhash}`;
    },
    ...mapGetters(["currentPair"]),
    ...mapState(["currentAccount"]),
  },
  mounted() {
    this.token = this.currentPair.tokens[0];
  },
  methods: {
    getAccountData() {
      return {
        from: this.currentAccount.address,
        token: this.token,
        amount: convertToWei(this.amount),
        isEth: this.isEth,
      };
    },

    // @todo: add deposit and withdraw for local wallets
    async deposit() {
      if (!this.amount) return;
      this.trasnactionData = await exchange.deposit(this.getAccountData());
      this.showTransactionModal = true;
    },
    async withdraw() {
      if (!this.amount) return;
      this.trasnactionData = await exchange.withdraw(this.getAccountData());
      this.showTransactionModal = true;
    },
    menageDeposit() {
      if (this.isWithdraw) {
        this.showWithdorawAlert = true;
      } else {
        this.deposit();
      }
    },
  },
};
</script>