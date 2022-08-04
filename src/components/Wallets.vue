<template>
  <div class="apps__item wallets">
    <img
      v-if="!currentAccount.metamask"
      src="../assets/wallet-white.svg"
      alt="wallet-white"
    />
    <img v-else src="../assets/wallet.svg" alt="" />
    <tooltip class="wallets-tooltip">
      <form
        @submit.prevent="imortKey"
        class="input-import"
        v-if="showImportKeyForm"
      >
        <input
          @keyup.enter="imortKey"
          :class="{ err: incorrectKey }"
          class="input-import__input"
          placeholder="privateKey_"
          type="text"
          v-model="importedPrivateKey"
        />
        <button type="submit" class="input-import__btn">import</button>
        <i class="input-import__cancel-btn">
          <svg
            @click="hideImportKeyForm()"
            width="10"
            height="10"
            xmlns="http://www.w3.org/2000/svg"
            version="1.1"
            xmlns:xlink="http://www.w3.org/1999/xlink"
            viewBox="0 0 10 10"
          >
            <g transform="matrix(1,0,0,1,-351,-64)">
              <path
                d="M352,72.07107l3.18198,-3.18198l-3.18198,-3.18198l0.7071,-0.70711l3.18198,3.18198l3.18198,-3.18198l0.7071,0.70711l-3.18198,3.18198l3.18198,3.18198l-0.70711,0.7071l-3.18197,-3.18198l-3.18198,3.18198z"
                fill-opacity="0"
                fill="#ffffff"
                stroke-linejoin="miter"
                stroke-linecap="butt"
                stroke-opacity="1"
                stroke="#ffffff"
                stroke-miterlimit="50"
                stroke-width="1"
                id="Path-0"
              ></path>
            </g>
          </svg>
        </i>
      </form>
      <div v-else class="wallet-container keys-container">
        <div class="gasPrice">
          <span>GAS PRICE: {{ gasPrice }}</span>
          <input
            class="gasrange"
            type="range"
            v-model="gasPrice"
            min="1"
            max="99"
            name="gas"
            id="gas"
          />
        </div>
        <div
          v-for="account in localAccounts"
          :key="account.address"
          class="wallet-container__item"
        >
          <div class="wallet_radio">
            <input
              type="radio"
              :checked="account.address == currentAccount.address"
              :id="account.address"
              :value="account.address"
              @change="setCurrentAccount(account)"
            />
            <label
              :class="{ active: currentAccount.address == account.address }"
              :value="account.address"
              :for="account.address"
            >
            </label>
          </div>
          <div v-if="account.privateKey" class="input-wallet">
            <input
              readonly
              :value="account.address"
              :id="account.address"
              class="input-wallet__address"
              type="text"
            />
            <input
              readonly
              :value="account.privateKey"
              :id="account.privateKey"
              class="input-wallet__private-key"
              type="text"
            />
            <button
              @click.prevent="copyToClipboard(account.address)"
              class="input-wallet__btn"
            >
              <img src="../assets/copy-ico.svg" alt="" />
            </button>
            <button
              @click.prevent="copyToClipboard(account.privateKey)"
              class="input-wallet__btn"
            >
              <img src="../assets/private-key.svg" alt="" />
            </button>
            <button
              @click.prevent="showDeleteModal(account)"
              class="input-wallet__btn"
            >
              <img src="../assets/trash.svg" alt="" />
            </button>
          </div>
        </div>

        <div v-if="showButtons" class="buttuns-container">
          <button @click="createAccount" class="generate-btn btn">
            GENERATE
          </button>
          <button
            @click.prevent="showImportKeyForm = true"
            class="import-btn btn"
          >
            IMPORT
          </button>
        </div>
      </div>
      <div
        v-if="metamaskAccount && accounts.length"
        class="wallet-container metamask-container"
      >
        <div class="wallet-container__item">
          <div class="wallet_radio">
            <input
              :value="metamaskAccount.address"
              type="radio"
              :id="metamaskAccount.address"
              @change="setCurrentAccount(metamaskAccount)"
            />
            <label
              :class="{ active: currentAccount == metamaskAccount }"
              :for="metamaskAccount.address"
            >
            </label>
          </div>
          <div class="input-wallet">
            <input
              readonly
              :value="metamaskAccount.address"
              class="input-wallet__address"
              type="text"
            />
            <button
              @click.prevent="copyToClipboard(metamaskAccount.address)"
              class="input-wallet__btn"
            >
              <img src="../assets/copy-ico.svg" alt="" />
            </button>
            <img
              class="metamask-img"
              width="18px"
              src="../assets/metaMask.svg"
              alt=""
            />
          </div>
        </div>
      </div>
    </tooltip>
    <alert v-if="isModalShown" @close="hideDeleteModal">
      <p>Do you want to delete account</p>
      <p>{{ accountToDelete.address }}</p>
      <div class="wallets__delete-buttons">
        <button
          @click="confirmDeleteAccount(accountToDelete)"
          class="btn btn-success"
        >
          Confirm
        </button>
        <button @click="hideDeleteModal" class="btn btn-secondary">
          Cancel
        </button>
      </div>
    </alert>
  </div>
</template>

<script>
import { mapActions, mapGetters, mapMutations, mapState } from "vuex";
import Tooltip from "./Tooltip.vue";
import Alert from "./Alert.vue";

export default {
  components: {
    Tooltip,
    Alert,
  },
  data() {
    return {
      newAccount: false,
      gasPrice: 5,
      importedPrivateKey: "",
      incorrectKey: false,
      showImportKeyForm: false,
      accountToDelete: null,
      isModalShown: false,
    };
  },
  computed: {
    showButtons() {
      return this.localAccounts.length !== 5;
    },
    ...mapState(["accounts", "currentAccount"]),
    ...mapGetters(["metamaskAccount", "localAccounts"]),
  },
  methods: {
    hideImportKeyForm() {
      this.showImportKeyForm = false;
      this.importedPrivateKey = "";
    },
    imortKey() {
      if (this.importedPrivateKey.length > 64) {
        this.importAccount(this.importedPrivateKey);
        this.importedPrivateKey = "";
        this.newAccount = false;
        this.incorrectKey = false;
      } else {
        this.incorrectKey = true;
      }
    },
    copyToClipboard(text) {
      navigator.clipboard.writeText(text);
    },
    showDeleteModal(account) {
      this.accountToDelete = account;
      this.isModalShown = true;
    },
    confirmDeleteAccount() {
      this.deleteAccount(this.accountToDelete);
      this.hideDeleteModal();
    },
    hideDeleteModal() {
      this.isModalShown = false;
      this.accountToDelete = null;
    },
    ...mapActions(["createAccount", "importAccount"]),
    ...mapMutations(["setCurrentAccount", "deleteAccount"]),
  },
};
</script>