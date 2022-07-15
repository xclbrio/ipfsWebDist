<template>
	<main>
		<transition name="fade">
			<loader v-if="preLoader"></loader>
		</transition>
		<main class="workflow">
			<keep-alive>
				<headerMain
					:from="from"
					:pair="pair"
				></headerMain>
			</keep-alive>
			<orederbook
				:pair="pair"
				:from="from"
				:contract="contract"
			></orederbook>
			
			<div class="window charts-tabs">
				<vue-tabs>
					<v-tab title="PRICE CHART">
						<keep-alive>
							<chart :pair="pair"></chart>
						</keep-alive>
					</v-tab>
					<v-tab title="DEPTH (SOON)">
						<depth></depth>
					</v-tab>
				</vue-tabs>
			</div>
			<history
				ref="history"
				:pair="pair"
				:from="from">
			</history>
			<forms 
				ref="forms"
				:pair="pair"
				:from="from" >
			</forms>
			<chat :from="from" :web3="web3" ref="chat"></chat>
		</main>
	</main>
</template>

<script>
	import exchange from '../exchange.js'
	import settings from '../settings.json'
	import Tx from 'ethereumjs-tx'
	import EthUtil from 'ethereumjs-util'
	import {VueTabs, VTab} from 'vue-nav-tabs'
	import headerMain from './header.vue'
	import orederbook from './orederbook.vue'
	import history from './history.vue'
	import chat from './chat.vue'
	import chart from './chart.vue'
	import depth from './depth.vue'
	import forms from './forms.vue'
	import loader from './loader.vue'

	export default {
		data(){
			return{
				pairs: settings.pairs,
				from: null,
				tabName: '',
				preLoader: true,
				accounts: [],
				metamaskAccount: '',
				gasPrice: 5,
			}
		},
		computed: {
			web3(){ 
				return web3;
			},
			currentAccount(){
				 
				return this.accounts.find(element => element.address == this.from);
			},
			privateKeyBuffer(){
				 
				return EthUtil.toBuffer(this.privateKey);
			},
			privateKey(){
				 
				return this.walletType ? '' : this.currentAccount.privateKey;
			},
			walletType(){
				return this.from == this.metamaskAccount
			},
			contract(){
				 
				return new this.web3.eth.Contract(settings.exchangeAbi, settings.exchangeAddress);
			},
			room(){
				return {
					pair: this.pair.path,
					t1: this.pair.tokens[0],
					t2: this.pair.tokens[1],
				}
			},
			lastDeal(){ 
				return this.$refs.history.historyData[0];
			}, 
			pairID(){
				return this.$route.params.id
			},
			pair(){
				return this.pairs.find(x => x.path == this.pairID)
			},
			defaultAccount(){
				this.web3.eth.defaultAccount = this.from
				return this.web3.eth.defaultAccount
			}
		},
		sockets:{
			connect(){
				 
				console.log('socket connected');
				
				this.$socket.emit('joinRoom', this.room);
				this.preLoader = false

			},
			trade(trade) {
				console.log('trade:', trade);
			}
		},
		watch: {
			pair() {
				 
				this.$socket.emit('joinRoom', this.room);
				console.log(this.room)
			},

		},
		components: {
			loader,
			headerMain,
			orederbook,
			chat,
			history,
			forms,
			chart,
			depth,
			VueTabs,
			VTab,
		},
		methods: {
			getAccounts(){
				if (localStorage.getItem('accounts') == null) {
					return []
				} else{
					return JSON.parse(localStorage.getItem('accounts'))
				}
			},
		},
		created(){
			 

			

			this.accounts = this.getAccounts();

			console.log(this.contract)

			try{
				this.web3.eth.getAccounts()
					.then(res => {
						// this.from = res[0];
						this.metamaskAccount = res[0];
						try {
							var curAcc = this.accounts.find(el => el.address == this.from).address
						} catch(e) {
							var curAcc = null;
						}

						if (this.from == null) {
							this.from = this.metamaskAccount;
						}

						if (this.from !== curAcc) {

							this.from = this.from == undefined ? this.accounts[0].address : this.metamaskAccount;
						}
					});

				this.web3.currentProvider.publicConfigStore.on('update', function() {
					this.web3.eth.getAccounts()
					.then(res => {
						// this.from = res[0];
						this.metamaskAccount = res[0];
						try {
							var curAcc = this.accounts.find(el => el.address == this.from).address
						} catch(e) {
							var curAcc = null;
						}

						if (this.from == null) {
							this.from = this.metamaskAccount;
						}

						if (this.from !== curAcc) {

							this.from = this.from == undefined ? this.accounts[0].address : this.metamaskAccount;
						}
					});
				});
			}catch(e){
				console.log(e)
			}

		},
	}
</script>

<style lang="scss">
	@import '../_base.scss';

	::-webkit-scrollbar {
		width: 0px;  /* remove scrollbar space */
		background: transparent;  /* optional: just make scrollbar invisible */
		display: none;

	}
	/* optional: show position indicator in red */
	::-webkit-scrollbar-thumb {
		background: $black-three;
	}

	input[type=number] { 
		-moz-appearance: textfield;
		appearance: textfield;
		margin: 0; 
		&::-webkit-inner-spin-button, 
		&::-webkit-outer-spin-button { 
			-webkit-appearance: none; 
			margin: 0; 
		}
	}
	.charts{
		width: 100%;
		display: flex;
		flex-direction: column;
	}
	.charts-tabs{
		flex: 6 0;
		display: flex;
	}
	.workflow{
		display: grid;
		height: 100vh;
		grid-gap: 1px;
		grid-template-columns: 378px  1fr  378px;
		grid-template-rows:	46px 6fr 4fr;
		grid-template-areas: "he he he" "od ct fo" "od hi ch";
		box-sizing: border-box;
	}

	.header{
		grid-area: he;
	}
	.orederbook{
		grid-area: od;
	}
	.charts-tabs{
		grid-area: ct;
	}
	.history{
		grid-area: hi;
	}
	.forms{
		grid-area: fo;
	}
	.chat{
		grid-area: ch;
	}
	.window{
		padding: 14px 5px 5px 5px;
		background-color: $black-three;
		color: #fff;
		border: 1px solid  $black;
		box-sizing: border-box;
		transition: 0.8s;
		overflow: hidden;
	}
	.window{
		padding: 14px 5px 5px 5px;
		background-color: $black-three;
		color: #fff;
		border: 1px solid  $black;
		box-sizing: border-box;
		transition: 0.8s;
		overflow: hidden;
	}
	.aside-left,
	.aside-right{
		height: 100%;
		display: flex;
		flex-direction: column;
	}
	.aside-left{
		width: 378px;
	}
	.active{
		.chat{
			flex: 1 0;
		}
		.forms{
			flex: 0 0 46px;
		}
	}
	@media screen and (max-width: 768px){
		.workflow,
		.header{
			flex-wrap: wrap;
			padding-top: 10px;
		}
		.header__balances,
		.header__langswitcher{
			display: none;
		}
		.workflow{
			padding-top: 20px;
		}
		.orederbook{
			width: 100% !important;
		}
		.forms{
			display: none;
		}
		.charts-tabs{
			height: 500px;
		}
		.main-section{
			order: 1;
		}
		.aside-left{
			order: 2;
			width: 50%;
		}
		.aside-right{
			order: 3;
			width: 50%;
		}
	}
	@media screen and (max-width: 425px){
		.aside-left,
		.aside-right{
			width: 100%;
		}
		.chat{
			width: 100%;
			flex: 0 0 400px;
		}
		.header__cotainer{
			flex-wrap: wrap;
			flex-direction: column;
		}
		.header__pairs{
			margin: 0;
		}
	}
</style>