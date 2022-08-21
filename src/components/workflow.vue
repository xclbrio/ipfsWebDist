<template>
  <main>
    <transition name="fade">
      <loader v-if="preLoader"></loader>
    </transition>
    <main class="workflow">
      <keep-alive>
        <headerMain />
      </keep-alive>
      <orederbook :pair="currentPair" />

      <div class="window charts-tabs">
        <vue-tabs>
          <v-tab title="PRICE CHART">
            <keep-alive>
              <chart :pair="currentPair" />
            </keep-alive>
          </v-tab>
          <v-tab disabled title="DEPTH (SOON)">
            <depth />
          </v-tab>
        </vue-tabs>
      </div>
      <history ref="history" :pair="currentPair" />
      <trade ref="forms" :pair="currentPair" />
      <chat ref="chat" />
    </main>
  </main>
</template>

<script>
import { VueTabs, VTab } from "vue-nav-tabs";
import headerMain from "@/components/header.vue";
import orederbook from "@/components/orederbook.vue";
import history from "@/components/history.vue";
import chat from "@/components/chat.vue";
import chart from "@/components/chart.vue";
import depth from "@/components/depth.vue";
import Trade from "@/components/Trade.vue";
import loader from "@/components/loader.vue";
import { mapActions, mapGetters, mapState } from "vuex";

export default {
  components: {
    loader,
    headerMain,
    orederbook,
    chat,
    history,
    Trade,
    chart,
    depth,
    VueTabs,
    VTab,
  },
  data() {
    return {
      tabName: "",
      preLoader: false,
      metamaskAccount: "",
      gasPrice: 5,
    };
  },
  computed: {
    lastDeal() {
      return this.$refs.history.historyData[0];
    },
    currentPairData() {
      return {
        pair: this.currentPair.path,
        t1: this.currentPair.tokens[0],
        t2: this.currentPair.tokens[1],
      };
    },
    ...mapState(["accounts", "currentAccount"]),
    ...mapGetters(["currentPair"]),
  },
  sockets: {
    connect() {
      this.$socket.emit("joinRoom", this.currentPairData);
      this.preLoader = false;
    },
  },
  watch: {
    currentPair() {
      this.$socket.emit("joinRoom", this.currentPairData);
    },
  },
  methods: {
    ...mapActions(["getAccounts"]),
  },
  created() {
    this.getAccounts();
  },
};
</script>

<style lang="scss">
@import "../_base.scss";

::-webkit-scrollbar {
  width: 0px; /* remove scrollbar space */
  background: transparent; /* optional: just make scrollbar invisible */
  display: none;
}
/* optional: show position indicator in red */
::-webkit-scrollbar-thumb {
  background: $black-three;
}

input[type="number"] {
  -moz-appearance: textfield;
  appearance: textfield;
  margin: 0;
  &::-webkit-inner-spin-button,
  &::-webkit-outer-spin-button {
    -webkit-appearance: none;
    margin: 0;
  }
}
.charts {
  width: 100%;
  display: flex;
  flex-direction: column;
}
.charts-tabs {
  flex: 6 0;
  display: flex;
}
.workflow {
  display: grid;
  height: 100vh;
  grid-gap: 1px;
  grid-template-columns: 378px 1fr 378px;
  grid-template-rows: 46px 6fr 4fr;
  grid-template-areas: "he he he" "od ct fo" "od hi ch";
  box-sizing: border-box;
}

.header {
  grid-area: he;
}
.orederbook {
  grid-area: od;
}
.charts-tabs {
  grid-area: ct;
}
.history {
  grid-area: hi;
}
.forms {
  grid-area: fo;
}
.chat {
  grid-area: ch;
}
.window {
  padding: 14px 5px 5px 5px;
  background-color: $black-three;
  color: #fff;
  border: 1px solid $black;
  box-sizing: border-box;
  transition: 0.8s;
  overflow: hidden;
}
.aside-left,
.aside-right {
  height: 100%;
  display: flex;
  flex-direction: column;
}
.aside-left {
  width: 378px;
}
.active {
  .chat {
    flex: 1 0;
  }
  .forms {
    flex: 0 0 46px;
  }
}
@media screen and (max-width: 768px) {
  .workflow,
  .header {
    flex-wrap: wrap;
    padding-top: 10px;
  }
  .header__balances,
  .header__langswitcher {
    display: none;
  }
  .workflow {
    padding-top: 20px;
  }
  .orederbook {
    width: 100% !important;
  }
  .forms {
    display: none;
  }
  .charts-tabs {
    height: 500px;
  }
  .main-section {
    order: 1;
  }
  .aside-left {
    order: 2;
    width: 50%;
  }
  .aside-right {
    order: 3;
    width: 50%;
  }
}
@media screen and (max-width: 425px) {
  .aside-left,
  .aside-right {
    width: 100%;
  }
  .chat {
    width: 100%;
    flex: 0 0 400px;
  }
  .header__cotainer {
    flex-wrap: wrap;
    flex-direction: column;
  }
  .header__pairs {
    margin: 0;
  }
}
</style>