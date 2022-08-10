<template>
  <div class="forms__content">
    <form @submit.prevent="postOrder()" class="forms__box form__buy">
      <div class="form__buy__amount">
        <p class="input__title">AMOUNT</p>
        <p class="input__contaner --amount">
          <input
            v-model.number="amount"
            placeholder="amount_"
            type="number"
            step="any"
            required
          />
          <span class="symbol-tooltip">{{ currentPair.symbols[0] }}</span>
        </p>
      </div>
      <div class="form__buy__price">
        <p class="input__title">PRICE</p>
        <p class="input__contaner --price">
          <input
            v-model.number="price"
            placeholder="price_"
            type="number"
            step="any"
            required
          />
          <span class="symbol-tooltip">{{ currentPair.symbols[1] }}</span>
        </p>
      </div>
      <p class="--greyish">
        TOTAL = <span class="--white">{{ total }}</span>
        {{ currentPair.symbols[1].toUpperCase() }}
      </p>
      <p class="--greyish">
        CHOOSE EXPIRES:
        <span
          v-for="item in expireses"
          :key="`${item.blockAmount}${isSellOrder ? 'sell' : 'buy'}`"
        >
          <input
            class="radio-btn"
            type="radio"
            :id="item.title"
            :value="item.title"
            v-model="expires"
          />
          <label
            :class="{ active: expires == item.title }"
            class="expries"
            :for="item.title"
            >{{ item.title }}</label
          >
        </span>
      </p>
      <div class="button-container">
        <button type="submit" :class="{ sell: isSellOrder }" class="button">
          <img
            v-if="isLoading"
            class="button__loader"
            src="../assets/loader.svg"
            alt="loader"
          />
          <template v-else>
            PLACE {{ isSellOrder ? "SELL" : "BUY" }} ORDER
          </template>
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import { mapGetters, mapState } from "vuex";
import { blockSpeed } from "@/settings.json";
import { web3 } from "@/services/connectWeb3";
import { convertToWei } from "@/services/helpers";
import exchange from "@/exchange";

export default {
  props: {
    isSellOrder: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      expires: "1H",
      price: null,
      amount: null,
      isLoading: false,
    };
  },
  computed: {
    expireses() {
      return [
        {
          title: "1H",
          time: 3600000,
          blockAmount: parseFloat((3600 / blockSpeed).toFixed(0)),
        },
        {
          title: "1D",
          time: 86400000,
          blockAmount: parseFloat((86400 / blockSpeed).toFixed(0)),
        },
        {
          title: "1W",
          time: 604800000,
          blockAmount: parseFloat((604800 / blockSpeed).toFixed(0)),
        },
      ];
    },
    currentExpires() {
      return this.expireses.find(({ title }) => this.expires === title);
    },
    total() {
      return (this.amount * this.price).toFixed(10);
    },
    ...mapGetters(["currentPair"]),
    ...mapState(["currentAccount"]),
  },
  methods: {
    async postOrder() {
      if (!this.amount || !this.price) return;
      const expires = await web3.eth
        .getBlockNumber()
        .then((blockNumber) => blockNumber + this.currentExpires.blockAmount);
      const expiresDateTime = new Date().getTime() + this.currentExpires.time;
      const [tokenGet, tokenGive] = this.isSellOrder
        ? this.currentPair.tokens.reverse()
        : this.currentPair.tokens;
      const { sign, hash, nonce } = await exchange.getSign(
        this.currentAccount.address,
        this.currentAccount.privateKey,
        tokenGet,
        tokenGive,
        convertToWei(this.total),
        convertToWei(this.amount),
        expires
      );

      this.$socket.emit("pushOrder", {
        orderType: this.isSellOrder ? "sell" : "buy",
        pair: this.currentPair.path,
        maker: this.currentAccount.address.toLowerCase(),
        amountGet: convertToWei(this.total),
        amountGive: convertToWei(this.amount),
        tokenGet,
        tokenGive,
        price: this.price,
        orderFills: convertToWei(this.total),
        sig: sign,
        expiresTime: Date(),
        nonce,
        expires,
        hash,
        expiresDateTime,
      });
    },
  },
};
</script>