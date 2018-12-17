	<template>
	<div class="window forms">
		<vue-tabs>
			<v-tab title="BUY">
				<div class="forms__content">
					<form class="forms__box form__buy">
						<div class="form__buy__amount">
							<p class="input__title">AMOUNT</p>
							<p class="input__contaner --amount"><input v-model="buyAmount" placeholder="amount_" type="number" step="0.001"><span class="symbol-toolkit">{{pair.symbols[0]}}</span></p>
						</div>
						<div class="form__buy__price">
							<p class="input__title">PRICE</p>
							<p class="input__contaner --price"><input @click="updatePrice = false" onClick="this.select();" v-model="buyPrice" placeholder="price_" type="number" step="0.001"><span class="symbol-toolkit">{{pair.symbols[1]}}</span></p>
						</div>
						<p class="--greyish">TOTAL = <span class="--white">{{buyTotal.noExponents()}}</span> {{pair.symbols[1].toUpperCase()}}</p>
						<p class="--greyish">CHOOSE EXPIRES: 
							<span v-for="item in expires">
								<input class="radio-btn" type="radio" :id="item.title" :value="item.blockAmount" v-model="picked">
								<label :class="{active: picked == item.blockAmount}" class="expries " :for="item.title">{{item.title}}</label>
							</span>
						</p>
						<p class="button-container"><button :disabled="buyLoader" @click.prevent="postOrder(token1, token2, buyAmount, buyTotal, 1)" class="button"><img v-if="buyLoader" class="button__loader" src="../assets/loader.svg" alt=""><span v-else class="button__text">PLACE BUY ORDER</span></button></p>
					</form>
				</div>
			</v-tab>

			<v-tab title="SELL">
				<div class="forms__content">	
					<form class="forms__box form__sell">
						<div class="form__buy__amount">
							<p class="input__title">AMOUNT</p>
							<p class="input__contaner --amount"><input v-model="sellAmount" placeholder="amount_" type="number" step="0.001"><span class="symbol-toolkit">{{pair.symbols[0]}}</span></p>
						</div>
						<div class="form__buy__price">
							<p class="input__title">PRICE</p>
							<p class="input__contaner --price"><input @click="updatePrice = false" onClick="this.select();" v-model="sellPrice" placeholder="price_" type="number" step="0.001"><span class="symbol-toolkit">{{pair.symbols[1]}}</span></p>
						</div>
						<p class="--greyish">TOTAL = <span class="--white">{{sellTotal.noExponents()}}</span> {{pair.symbols[1].toUpperCase()}}</p>
						<p class="--greyish">CHOOSE EXPIRES: 
							<span v-for="item in expires">
								<input class="radio-btn" type="radio" :id="item.title" :value="item.blockAmount" v-model="picked">
								<label :class="{active: picked == item.blockAmount}" class="expries" :for="item.title">{{item.title}}</label>
							</span>
						<p class="button-container"><button :disabled="sellLoader" @click.prevent="postOrder(token2, token1, sellTotal, sellAmount, 0)" class="button sell"><img v-if="sellLoader" class="button__loader" src="../assets/loader.svg" alt=""><span v-else class="button__text">PLACE SELL ORDER</span></button></p>
					</form>
				</div>	
			</v-tab>

			<v-tab title="MANAGE">
				<div class="forms__content">
					<form class="forms__box form__manage">
						<div class="form__sell__deposit">
							<p class="--greyish input__title">DEPOSIT -><span v-for="item in tokensData"><input 
								class="radio-btn"  
								type="radio"  
								:id="item.name"  
								:value="item.token"  
								v-model="depositToken"><label  
								:class="{active: depositToken == item.token}"  
								class="expries " 
								:for="item.name">{{item.name}}</label></span>[choose currency]</p>
								<p class="input__contaner --amount"><input v-model="depositAmount" placeholder="amount_" type="number" step="0.001"><button @click.prevent="deposit" class="btn btn_deposit">SEND</button></p>
						</div>
					</form>
					<form class="forms__box form__manage">
						<div class="form__sell__withdraw">
							<p class="--greyish input__title">WITHDRAW -><span v-for="item in tokensData"><input
								class="radio-btn" 
								type="radio" 
								:id="item.token" 
								:value="item.token" 
								v-model="withdrawToken"><label 
								:class="{active: withdrawToken == item.token}" 
								class="expries" 
								:for="item.token">{{item.name}}</label></span>[choose currency]</p>
							<p class="input__contaner --amount"><input v-model="withdrawAmount" placeholder="amount_" type="number" step="0.001"><button @click.prevent="withdrawAlert" class="btn btn_deposit">SEND</button></p>
						</div>
					</form>
				</div>
			</v-tab>
		</vue-tabs>

		<alert ctx="error" :title="errorTitle" v-show="popup">
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
		<alert v-show="withdrawBool" ctx="error" title="ATTENTION">
			<p class="withdraw-alert"><span>All your orders will be deleted!</span> <button @click.prevent="withdraw" class="btn accept">Accept</button></p>
		</alert>
		<alert ctx="transaction" title="TRANSACTION" v-show="tx">
			<div class="copy-input">
				<div class="container"><input id="hash" ref="hash" v-model="txhash" type="text"><button @click.stop.prevent="copyHash" class="copy"><img src="../assets/copy-ico.svg" alt=""></button></div>
				<div class="etherscan"><a target="_blank" :href="txlink">VIEW ON ETHERSCAN</a></div>
			</div>
		</alert>
	</div>
</template>

<script>
	
	import exchange from '../exchange.js'
	import settings from '../settings.json'
	import exchangeLocal from '../exchangeLocal.js'
	import Tx from 'ethereumjs-tx'
	import EthUtil from 'ethereumjs-util'
	import alert from "./alert.vue"

	export default {
		name: 'forms',
		data(){
			return {
				settings: settings,
				depositToken: this.pair.tokens[0],
				withdrawToken: this.pair.tokens[0],
				buyAmount: '',
				buyPrice: '',
				sellAmount: '',
				sellPrice: '',
				depositAmount: null,
				withdrawAmount: null,
				hash: null,
				sign: null,
				updatePrice: true,


				spender: settings.exchangeAddress,

				picked: '',

				popup: false,
				withdrawBool: false,
				error: '',
				errorTitle: '',

				tx: false,
				txhash: '',
				buyLoader: false,
				sellLoader: false,
			}
		},
		components: {
			alert,
		},
		computed: {
			isDesibled(){
				return e
			},
			gasPrice(){
				return this.$parent.gasPrice;
			},
			web3(){
				return this.$parent.web3
			},
			contract(){
				const vm = this;
				return exchange.initContract(vm.web3, settings.exchangeAbi, settings.exchangeAddress);
			},
			token1(){ return this.pair.tokens[0]},
			token2(){ return this.pair.tokens[1]},
			txlink(){ return `${settings.network.etherscan}tx/${this.txhash}`},
			blockSpeed(){ return this.settings.blockSpeed},
			expires(){
				return [
					{
						title: '1H',
						time: 3600000,
						blockAmount: parseFloat((3600 / this.blockSpeed).toFixed(0)),
					},
					{
						title: '1D',
						time: 86400000,
						blockAmount: parseFloat((86400 / this.blockSpeed).toFixed(0)),
					},
					{
						title: '1W',
						time: 604800000,
						blockAmount: parseFloat((604800 / this.blockSpeed).toFixed(0)),
					}
				]
			},
			pickedExpires(){
				const vm = this;
				return this.expires.find(el => el.blockAmount == vm.picked)
			},
			lastDeal(){
				return this.$parent.lastDeal
			},
			tokensData(){
				return [
					{
						name: this.pair.symbols[0],
						token: this.pair.tokens[0],
					},
					{
						name: this.pair.symbols[1],
						token: this.pair.tokens[1],
					}
				]
			},
			resource() {
	            return this.$resource('https://exapi1.herokuapp.com/v0.1/pushOrder')
	        },
			buyTotal(){
				var res = this.buyAmount * this.buyPrice;
				return +res.toFixed(6);
			},
			sellTotal(){
				var res = this.sellAmount * this.sellPrice; 
				return +res.toFixed(6);
			},
		},
		watch: {
			lastDeal(){
				this.buyPrice = '';
				this.sellPrice = '';
				this.getPrice();
			},
			tokensData(){
				this.depositToken = this.pair.tokens[0];
				this.withdrawToken = this.pair.tokens[0];
			},
			pair(){
				this.updatePrice = true;
				this.buyPrice = '';
				this.sellPrice = '';
				console.log("something changed")
				this.getPrice();
			},
		},
		sockets: {
			error(error){
				this.buyLoader = false;
				this.sellLoader = false;
				error = String(error);

				console.log(error)
				if (~error.indexOf('error')) {
					// location.reload();
				}else{
					this.popup = true;
					this.errorTitle = `Error ${error}`
				}
			},
			trade(trade){
				if (this.updatePrice) {
					this.buyPrice = '';
					this.getPrice();
				}
			},
			pushOrder(pushOrder){
				const vm = this;
				if(pushOrder.sig == vm.sign){
					vm.buyAmount = '';
					vm.sellAmount = '';
					if(pushOrder.orderType == 1){
						setTimeout(() => {
							vm.buyLoader = false;
						},2500)
					}else{
						setTimeout(() => {
							vm.sellLoader = false;
						},2500)
					}
				}
			}
		},
		props:{
			pair: Object,
			from: String,
		},
		methods: {
			// slideDownChat(){
			// 	var chat = document.querySelector('.aside-right')
			// 	chat.classList.remove('active')
			// },
			closePopup(){
				this.popup = false;
				this.tx = false;
				this.withdrawBool = false;
			},
			getPrice(){
				const vm = this;
				try {
					vm.buyPrice = vm.updatePrice == true ? vm.lastDeal.price : vm.buyPrice;
					vm.sellPrice = vm.updatePrice == true ? vm.lastDeal.price : vm.sellPrice;
				} catch(e) {
					console.log(e);
				}
			},
			depositMetamask(){
				const vm = this
				if (this.depositToken == '0x0000000000000000000000000000000000000000') {
					exchange.deposit(this.contract, this.from, web3.utils.toWei(vm.depositAmount.toString()), function(h){
						if (h !== "undefined") {
							vm.txhash = String(h);
							vm.tx = true;
						}
					}).then(res => console.log(res), err => console.log(err))
				}else{
					(async function () {
						const contract = exchange.initContract(vm.web3, settings.tokenAbi, vm.depositToken)
						console.log(contract)
						await exchange.depositToken(vm.contract, contract, vm.from, vm.spender, vm.depositToken, web3.utils.toWei(vm.depositAmount.toString()), function(h){
							if (h !== "undefined") {
								vm.txhash = String(h);
								vm.tx = true;
							}
						}).then(res => console.log(res), err => console.log(err))
					})()
				}
			},
			depositLocal(){
				const vm = this
				var amount = web3.utils.toWei(vm.depositAmount.toString())
				if (this.depositToken == '0x0000000000000000000000000000000000000000') {
					exchangeLocal.depositLocal(vm.web3, Tx, vm.contract, vm.spender, vm.from, vm.$parent.privateKeyBuffer, vm.gasPrice, EthUtil.toBuffer(amount),  function(h){
							if (h !== "undefined") {
								vm.txhash = String(h);
								vm.tx = true;
							}
						})
				}else{
					const tokenContract = new vm.web3.eth.Contract(settings.tokenAbi, vm.depositToken);
					exchangeLocal.depositTokenLocal(vm.web3, Tx, vm.contract, tokenContract, vm.spender, vm.depositToken, vm.from, vm.$parent.privateKeyBuffer, vm.gasPrice, amount, 0, function(h){
							if (h !== "undefined") {
								vm.txhash = String(h);
								vm.tx = true;
							}
						});
				}
			},
			deposit() {
				const vm = this
				if (this.$parent.walletType) {
					vm.depositMetamask();
				}else{
					vm.depositLocal();
				}
			},
			withdrawAlert(){
				const vm = this;
				if (vm.withdrawAmount !== null && vm.withdrawAmount !== '') {
					vm.withdrawBool = true;
					// console.log('ok')
				}
			},
			withdrawLocal(){
				const vm = this
				if (this.withdrawToken == '0x0000000000000000000000000000000000000000') {
					exchangeLocal.withdrawLocal(vm.web3, Tx, vm.contract, vm.spender, vm.from, vm.$parent.privateKeyBuffer, vm.gasPrice, web3.utils.toWei(vm.withdrawAmount.toString()), 0, function(h){
							if (h !== "undefined") {
								vm.txhash = String(h);
								vm.tx = true;
							}
						})
				}else{
					const tokenContract = new vm.web3.eth.Contract(settings.tokenAbi, vm.withdrawToken);
					exchangeLocal.withdrawTokenLocal(vm.web3, Tx, vm.contract, tokenContract, vm.spender, vm.withdrawToken, vm.from, vm.$parent.privateKeyBuffer, vm.gasPrice, web3.utils.toWei(vm.withdrawAmount.toString()), 0, function(h){
							if (h !== "undefined") {
								vm.txhash = String(h);
								vm.tx = true;
							}
						});
				}

			},
			withdrawMetamask(){
				const vm = this;
				if (vm.withdrawAmount !== null) {
					if (this.withdrawToken == '0x0000000000000000000000000000000000000000') {
						exchange.withdraw(this.contract, this.from, web3.utils.toWei(vm.withdrawAmount.toString()), function(h){
							if (h !== "undefined") {
								vm.txhash = String(h);
								vm.tx = true;
							}
						}).then(res => console.log(res), err => console.log(err))
					}else{
						exchange.withdrawToken(this.contract, this.from, this.withdrawToken, web3.utils.toWei(vm.withdrawAmount.toString()), function(h){
							if (h !== "undefined") {
								vm.txhash = String(h);
								vm.tx = true;
							}
						}).then(res => console.log(res), err => console.log(err))
					}
				}
			},
			withdraw() {
				const vm = this
				this.withdrawBool = false;
				if (this.$parent.walletType) {
					vm.withdrawMetamask();
				}else{
					vm.withdrawLocal();
				}
			},
			postOrder(tokenGet, tokenGive, amountGet, amountGive, orderType){
				const vm = this;
				(async function(){
					let nonce = Math.floor(Math.random() * 1000000) + 100
					let expires = null;
					let hash = null;
					await web3.eth.getBlockNumber().then(res => expires = res + parseFloat(vm.picked))
					if(vm.$parent.walletType){
						await exchange.getSign(vm.web3, vm.from, settings.exchangeAddress, tokenGet.toLowerCase(), web3.utils.toWei(amountGet.toString()), tokenGive.toLowerCase(), web3.utils.toWei(amountGive.toString()), expires, nonce, function(h){
							hash = h;
						}).then(res => vm.sign = res)
					}else{
						hash = exchange.orderHash(vm.web3, settings.exchangeAddress, tokenGet.toLowerCase(), web3.utils.toWei(amountGet.toString()), tokenGive.toLowerCase(), web3.utils.toWei(amountGive.toString()), expires, nonce);
						var signature = vm.web3.eth.accounts.sign(hash, vm.$parent.privateKey);
						vm.sign = signature.signature;
						vm.web3.eth.accounts.recover
					}
					if (orderType == 1) {
						vm.buyLoader = true;
					}else{
						vm.sellLoader = true;
					}
					let price = orderType == 1 ? parseFloat(amountGet) / parseFloat(amountGive) : parseFloat(amountGive) / parseFloat(amountGet);
					let date = new Date();
					vm.$socket.emit('pushOrder',{
					    "orderType": orderType,
					    "pair": vm.pair.path,
					    "maker": vm.from.toLowerCase(),
					    "tokenGet": tokenGet.toLowerCase(),
					    "amountGet": web3.utils.toWei(amountGet.toString()),
					    "tokenGive": tokenGive.toLowerCase(),
					    "amountGive": web3.utils.toWei(amountGive.toString()),
					    "price": price,
					    "expires": expires,
					    "nonce": parseFloat(nonce),
					    "orderFills": web3.utils.toWei(amountGet.toString()),
					    "hash": hash,
					    "sig": vm.sign,
					    "expiresTime": Date(),
					    "expiresDateTime": date.getTime() + vm.pickedExpires.time
					});
				})()
			},

		},
		created(){
			const vm = this;
			document.onerror = function(message, source, lineno, colno, error) {
				vm.popup = true;
				vm.errorTitle = message
				console.log(message)
			}

			// exchangeLocal.depositLocal(vm.web3, Tx, vm.contract, vm.spender, vm.from, vm.$parent.privateKeyBuffer, 5, (50 * 10**18).noExponents());

			this.picked = this.expires[0].blockAmount;
		},

	}
</script>

<style lang="scss">
	@import '../_base.scss';


	.--greyish{
		color: $greyish;
	}
	.--white{
		color: $white;
	}
	
	.reslove-container{
		display: flex;
		justify-content: space-between;
		align-items: center;
	}
	.support-btn{
		width: 245px;
		background-color: $algae-green;
		text-align: center;
		box-sizing: border-box;
		padding: 12px;
		cursor: pointer;
		color: $white;
	}
	.reslove{
		font-size: 12px;
		ul{
			list-style-type: none;
			padding: 0
		}
	}
	.withdraw-alert{
		display: flex;
		align-items: center;
		justify-content: space-between;
		.btn{
			width: 245px;
			height: 40px;
			background-color: $algae-green;
			display: flex;
			align-items: center;
			justify-content: center;
			border-radius: 0;
		}
	}
	.btn{
		background-color: $algae-green;
		color: $white;
		border: none;
		border-radius: 3px;
		width: 100px;
		text-align: center;
		outline: none;
		cursor: pointer;

		&:active{
			box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.5);
		}
	}
	.radio-btn{
		display: none;
	}
	.nav-tabs{
		list-style: none;
		padding: 0;
		margin: 0;
		display: flex;
		justify-content: space-between;
		align-items: center;
		width: 100%;

	}
	.forms__box{
		max-width: 350px;
		margin: 0 auto;
	}
	.tab{
		padding: 6px;
		width: 100%;
		text-align: center;
		&.active{
			background-color: $black-four;
		}
		a{
			color: $white;
			text-decoration: none;
		}
	}
	.forms{
		flex: 6 0;
		display: flex;
	}
	.tabs__item{
		text-transform: uppercase;
	}
	.forms__content{
		background-color: $black-four;
		padding: 22px;
		font-size: 14px;
		overflow-y: scroll;
		flex: 1;
	}
	.input__title{
		color: $greyish;
	}
	.symbol-toolkit{
		position: absolute;
		text-transform: uppercase;
		color: $greyish;
		right: 25px;
		top: 50%;
		transform: translateY(-50%);
	}
	.input__contaner{
		box-sizing: border-box;
		display: flex;
		position: relative;
		input{
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
	.form__buy{
		.expries{
			&.active{
				color: $algae-green;
			}
		}
	}
	.form__sell{
		.expries{
			&.active{
				color: $grapefruit;
			}
		}
	}
	.expries{
		margin: 5px;
		cursor: pointer;
		text-transform: uppercase;
	}
	.button-container{
		text-align: center;
		margin-top: 30px;
	}
	.btn_deposit{
		font-weight: 700;
	}
	@keyframes rotate{
		0% { 
			transform: rotate(0deg);
		}
		100% {
			transform: rotate(360deg);
		}
	}
	.button__loader{
		height: 30px;
		transform-origin: 50% 50%;
		animation: rotate 2s ease-in-out infinite;
	}
	.button{
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

		&:active{
			box-shadow: inset 0 1px 3px rgba(0,0,0,0.5);
		}
		&.sell{
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