	<template>
  <div class="window forms">
    <vue-tabs>
      <v-tab title="BUY">
        <order-placement />
      </v-tab>

      <v-tab title="SELL">
        <order-placement :isSellOrder="true" />
      </v-tab>

      <v-tab title="MANAGE">
        <div class="forms__content">
          <menage-deposit />
          <menage-deposit :isWithdraw="true" />
        </div>
      </v-tab>
    </vue-tabs>

    <alert
      ctx="error"
      :title="errorTitle"
      v-if="showErrorModal"
      @close="showErrorModal = false"
    >
      <div class="reslove-container">
        <div class="reslove">
          <div>PLEASE CHECK:</div>
          <ul>
            <li>* BALANCE</li>
            <li>* ORDER AMOUNT</li>
            <li>* METAMASK CONNECTION</li>
          </ul>
        </div>

        <div class="support-btn">SUPPORT</div>
      </div>
    </alert>
  </div>
</template>

<script>
import Alert from "@/components/Alert";
import OrderPlacement from "@/components/OrderPlacement";
import MenageDeposit from "@/components/MenageDeposit";
import { VueTabs, VTab } from "vue-nav-tabs";

export default {
  name: "Trade",
  components: {
    Alert,
    OrderPlacement,
    MenageDeposit,
    VueTabs,
    VTab,
  },
  data() {
    return {
      showErrorModal: false,
      error: "",
      errorTitle: "",
    };
  },
  sockets: {
    error(error) {
      this.buyLoader = false;
      this.sellLoader = false;
      error = String(error);
      if (~error.indexOf("error")) {
        // location.reload();
      } else {
        this.popup = true;
        this.errorTitle = `Error ${error}`;
      }
    }
  },
  methods: {
    slideDownChat() {
      const chat = document.querySelector(".aside-right");
      chat.classList.remove("active");
    },
  },
  created() {
    document.onerror = function (message, source, lineno, colno, error) {
      this.popup = true;
      this.errorTitle = message;
      console.log(message);
    };
  },
};
</script>

<style lang="scss">
@import "../_base.scss";

.--greyish {
  color: $greyish;
}
.--white {
  color: $white;
}

.reslove-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.support-btn {
  width: 245px;
  background-color: $algae-green;
  text-align: center;
  box-sizing: border-box;
  padding: 12px;
  cursor: pointer;
  color: $white;
}
.reslove {
  font-size: 12px;
  ul {
    list-style-type: none;
    padding: 0;
  }
}
.withdraw-alert {
  display: flex;
  align-items: center;
  justify-content: space-between;
  .btn {
    width: 245px;
    height: 40px;
    background-color: $algae-green;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 0;
  }
}
.btn {
  background-color: $algae-green;
  color: $white;
  border: none;
  border-radius: 3px;
  width: 100px;
  text-align: center;
  outline: none;
  cursor: pointer;

  &:active {
    box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.5);
  }
}
.radio-btn {
  display: none;
}
.nav-tabs {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}
.forms__box {
  max-width: 350px;
  margin: 0 auto;
}
.tab {
  padding: 6px;
  width: 100%;
  text-align: center;
  &.active {
    background-color: $black-four;
  }
  a {
    color: $white;
    text-decoration: none;
  }
}
.forms {
  flex: 6 0;
  display: flex;
}
.tabs__item {
  text-transform: uppercase;
}
.forms__content {
  background-color: $black-four;
  padding: 22px;
  font-size: 14px;
  overflow-y: scroll;
  flex: 1;
}
.input__title {
  color: $greyish;
}
.symbol-tooltip {
  position: absolute;
  text-transform: uppercase;
  color: $greyish;
  right: 25px;
  top: 50%;
  transform: translateY(-50%);
}
.input__contaner {
  box-sizing: border-box;
  display: flex;
  position: relative;
  input {
    display: block;
    box-sizing: border-box;
    border-radius: 3px;
    border: 1px solid $warm-grey;
    background-color: $greyish-brown;
    padding: 12px 25px;
    width: 100%;
    color: $white;
    outline: none;
  }
}
.form__manage,
.form__buy {
  .expries {
    &.active {
      color: $algae-green;
    }
  }
}
.form__sell {
  .expries {
    &.active {
      color: $grapefruit;
    }
  }
}
.expries {
  margin: 5px;
  cursor: pointer;
  text-transform: uppercase;
}
.button-container {
  text-align: center;
  margin-top: 30px;
}
.btn_deposit {
  font-weight: 700;
}
@keyframes rotate {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
.button__loader {
  height: 30px;
  transform-origin: 50% 50%;
  animation: rotate 2s ease-in-out infinite;
}
.button {
  border: none;
  width: 246px;
  height: 40px;
  background-color: $algae-green;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  box-sizing: border-box;
  text-transform: uppercase;
  color: $white;
  min-width: 246px;
  outline: none;
  cursor: pointer;
  font-weight: 700;

  &:active {
    box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.5);
  }
  &.sell {
    background-color: $grapefruit;
    color: $white;
  }
}
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  /* display: none; <- Crashes Chrome on hover */
  -webkit-appearance: none;
  margin: 0; /* <-- Apparently some margin are still there even though it's hidden */
}
</style>