<template>
	<header class="header">
		<div class="header__cotainer --left">
			<div v-if="ipfs" class="header__logo"><img src="../assets/excaliburLogoIPFS.svg" alt="excalibur_alpha" class="header__logo-img"></div>
			<div v-else class="header__logo"><img src="../assets/excaliburLogo.svg" alt="excalibur_alpha" class="header__logo-img"></div>
			<div class="header__pairs">
				<div v-on:click="dropdown = !dropdown" class="cur-pair">{{ pair.name }} <span><svg id="SVGDoc" width="14" height="7" xmlns="http://www.w3.org/2000/svg" version="1.1" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:avocode="https://avocode.com/" viewBox="0 0 14 7"><defs><path d="M283,20l-7,7l-7,-7v0" id="Path-0"/><clipPath id="ClipPath1016"><use xlink:href="#Path-0" fill="#ffffff"/></clipPath></defs><g transform="matrix(1,0,0,1,-269,-20)"><g><title>arrow</title><use xlink:href="#Path-0" fill-opacity="0" fill="#ffffff" stroke-linejoin="miter" stroke-linecap="butt" stroke-opacity="1" stroke="#aeaeae" stroke-miterlimit="50" stroke-width="2" clip-path="url(&quot;#ClipPath1016&quot;)"/></g></g></svg></span></div>

				<transition	name="slide">
					<ul v-if="dropdown" class="pairs">
						<li><input class="search-pair" type="text" placeholder="search_" v-model="search"></li>
						<li v-on:click="dropdown = !dropdown" v-for="item in filteredList" class="pair__item"><router-link :to="{ name: 'pair', params: { id: item.path }}">{{ item.name }}</router-link></li>
					</ul>
				</transition>
			</div>
			<div class="header__balances">
				<div class="balances__title">balances:</div>
				<div class="token-balances-list__item">
					<span class="amount">{{ amount1 }}</span>
					<span class="symbol"> {{ pair.symbols[0] }}, </span>
				</div>
				<div class="token-balances-list__item">
					<span class="amount">{{ amount2 }}</span> 
					<span class="symbol"> {{ pair.symbols[1] }}</span>
				</div>
			</div>
		</div>
		<div class="header__cotainer --right">
			<ul :class="menu" class="header__navi">
				<li class="header__navi-item --red"><a target="_blank" href="https://github.com/xclbrio/wiki/issues">report</a></li>
				<li class="header__navi-item"><a target="_blank" href="https://github.com/xclbrio">github</a></li>
				<li class="header__navi-item"><a target="_blank" :href="etherscan">etherscan</a></li>
				<li class="header__navi-item"><a target="_blank" href="https://twitter.com/xclbrio">twitter</a></li>
				<li class="header__navi-item"><a target="_blank" href="https://t.me/xclbrio">telegram</a></li>
			</ul>

			<!-- <div class="header__langswitcher">
				<div class="lang-switcher">EN <span>
					<svg id="SVGDoc" width="14" height="7" xmlns="http://www.w3.org/2000/svg" version="1.1" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:avocode="https://avocode.com/" viewBox="0 0 14 7">
						<defs>
							<path d="M283,20l-7,7l-7,-7v0" id="Path-0"/>
							<clipPath id="ClipPath1016"><use xlink:href="#Path-0" fill="#ffffff"/></clipPath>
						</defs>
						<g transform="matrix(1,0,0,1,-269,-20)">
							<use xlink:href="#Path-0" fill-opacity="0" fill="#ffffff" stroke-linejoin="miter" stroke-linecap="butt" stroke-opacity="1" stroke="#aeaeae" stroke-miterlimit="50" stroke-width="2" clip-path="url(&quot;#ClipPath1016&quot;)"/>
						</g>
					</svg>
				</span>
			</div>
		</div>
 -->
			<div class="apps">
				<div class="apps__item wallets">
					<img v-if="$parent.walletType == false && localAccounts.length > 0" src="../assets/wallet-white.svg" alt="">
					<img v-else src="../assets/wallet.svg" alt="">
					<toolkit class="wallets-toolkit">
						<form>
							<div v-if="!newAccount" class="wallet-container keys-container">
								<div class="gasPrice">
									<span>GAS PRICE: {{$parent.gasPrice}}</span>
									<input class="gasrange" type="range" v-model="$parent.gasPrice" min="1" max="99" name="gas" id="gas">
								</div>
							<div	v-for="item in localAccounts" class="wallet-container__item">
									<div class="wallet_radio">
										<input v-model="picked" type="radio" :id="item.address.substr(38, 42)" :value="item.address">
										<label :class="{active: picked == item.address}" :value="item.account" :for="item.address.substr(38, 42)"><i></i></label>
									</div>
									<div class="input-wallet">
										<input readonly="" :value="item.address" :id="item.address.substr(37, 42)" class="input-wallet__address" type="text">
										<input readonly="" :value="item.privateKey" :id="item.privateKey.substr(37, 42)" class="input-wallet__private-key" type="text">
										<button @click.prevent="copy(item.address.substr(37, 42))" class="input-wallet__btn"><img src="../assets/copy-ico.svg" alt=""></button>
										<button @click.prevent="copy(item.privateKey.substr(37, 42))" class="input-wallet__btn"><img src="../assets/private-key.svg" alt=""></button>
										<button @click.prevent="deleteWallet(item.address)" class="input-wallet__btn"><img src="../assets/trash.svg" alt=""></button>
									</div>
								</div>


								<div v-show="walletButtons" class="buttuns-container">
									<button @click.prevent="generateKey" class="generate-btn btn">GENERATE</button>
									<button @click.prevent="newAccount = true" class="import-btn btn">IMPORT</button>
								</div>
							</div>
							<div class="input-import" v-if="newAccount">
								<input @keyup.enter="imortKey" :class="{err: incorrectKey}" class="input-import__input" placeholder="privateKey_" type="text" name="account" v-model="newAccountKey" id="">
								<button @click.prevent="imortKey" class="input-import__btn">import</button>
								<i class="input-import__cancel-btn"><svg @click="closeInput()" width="10" height="10" xmlns="http://www.w3.org/2000/svg" version="1.1" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 10 10"><g transform="matrix(1,0,0,1,-351,-64)"><path d="M352,72.07107l3.18198,-3.18198l-3.18198,-3.18198l0.7071,-0.70711l3.18198,3.18198l3.18198,-3.18198l0.7071,0.70711l-3.18198,3.18198l3.18198,3.18198l-0.70711,0.7071l-3.18197,-3.18198l-3.18198,3.18198z" fill-opacity="0" fill="#ffffff" stroke-linejoin="miter" stroke-linecap="butt" stroke-opacity="1" stroke="#ffffff" stroke-miterlimit="50" stroke-width="1" id="Path-0"></path></g></svg></i>
							</div>

							<div v-if="metamask == 'metamask' && localAccounts.length > 0" class="wallet-container metamask-container">
								<div class="wallet-container__item">
									<div class="wallet_radio">
										<input v-model="picked" :value="metamaskAccount" type="radio" :id="metamaskAccount.substr(38, 42)">
										<label :class="{active: picked == metamaskAccount}" :for="metamaskAccount.substr(38, 42)"><i></i></label>
									</div>
									<div class="input-wallet">
										<input readonly="" :value="metamaskAccount" :id="metamaskAccount.substr(36, 42)" class="input-wallet__address" type="text">
										<button @click.prevent="copy(metamaskAccount.substr(36, 42))" class="input-wallet__btn"><img src="../assets/copy-ico.svg" alt=""></button>
										<img class="metamask-img" width="18px" src="../assets/metaMask.svg" alt="">
									</div>
								</div>
							</div>
						</form>
					</toolkit>
				</div>
				<div class="apps__item ledger__logo">
					<img src="../assets/ledger.svg" alt="">
					<toolkit class="ledger-toolkit">
						LEDGER <br>
						Available soon.
					</toolkit>
				</div>
				<div class="apps__item metamask__logo">
					<i class="ico" :class="metamask" alt=""></i>


					<toolkit class="metamask-toolkit">
						<div v-if="metamask == 'metamask'" class="metamask-continer">
							<div class="metamask-copy">
								<input id="address" :value="metamaskAccount" type="text">
								<button @click="copy('address')" class="copy"><img src="../assets/copy-ico.svg" alt=""></button>
							</div>
							<div class="indicators">
								<div class="condition --green">ACTIVE</div>
								<transition name="fade">
									<div v-if="copied">COPIED</div>
								</transition>
								<div class="network --purple">{{network.toUpperCase()}}</div>
							</div>
						</div>
						<div v-else class="metamask-container">
							<div class="title">METAMASK IS NOT AVAILABLE</div>
							<div class="extantion-container">
								<div class="--padding-left">Please unlock your wallet or install chrome extension.</div>
								<a target="_blank" href="https://chrome.google.com/webstore/detail/metamask/nkbihfbeogaeaoehlefnkodbefgpgknn?hl=en">INSTALL</a>
							</div>
						</div>
					</toolkit>
				</div>
			</div>
		</div>
		<div class="menu" @click="showMenu">
			<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" id="Layer_1" x="0px" y="0px" viewBox="0 0 512 512" style="enable-background:new 0 0 512 512;" xml:space="preserve" width="30px" height="30px">
				<g>
					<path id="path1" d="M491.318,235.318H20.682C9.26,235.318,0,244.577,0,256s9.26,20.682,20.682,20.682h470.636	c11.423,0,20.682-9.259,20.682-20.682C512,244.578,502.741,235.318,491.318,235.318z" fill="#FFFFFF"/>
					<path id="path2" d="M491.318,78.439H20.682C9.26,78.439,0,87.699,0,99.121c0,11.422,9.26,20.682,20.682,20.682h470.636	c11.423,0,20.682-9.26,20.682-20.682C512,87.699,502.741,78.439,491.318,78.439z" fill="#FFFFFF"/>
					<path id="path3" d="M491.318,392.197H20.682C9.26,392.197,0,401.456,0,412.879s9.26,20.682,20.682,20.682h470.636	c11.423,0,20.682-9.259,20.682-20.682S502.741,392.197,491.318,392.197z" fill="#FFFFFF"/>
				</g>
			</svg>
		</div>
		
	</header>
</template>

<script>
	import exchange from '../exchange.js'
	import settings from '../settings.json'

	import toolkit from './toolkit.vue'

	export default {
		name: 'headerMain',
		components: { toolkit, },
		data: function(){
			return {
				ipfs: ~location.href.toLowerCase().indexOf('ipfs'),
				newAccount: false,
				incorrectKey: false,
				newAccountKey: '',
				dropdown: false,
				amount1: '…',
				amount2: '…',
				alert: true,
				menu: '',
				network: settings.network.name,

				metamaskToolkit: false,
				ladgerToolkit: false,

				copied: false,

				picked: localStorage.getItem('currentAddress'),

				search: '',

			}

		},
		computed: {
			filteredList() {
				return this.pairs.filter(item => {
					return item.name.toLowerCase().includes(this.search.toLowerCase())
				})
			},
			web3() {
				return this.$parent.web3
			},
			metamaskAccount(){
				return this.$parent.metamaskAccount
			},
			localAccounts() {
				return this.$parent.accounts
			},
			walletButtons() {
				const vm = this;
				return vm.localAccounts.length !== 5
			},
			etherscan(){
				return settings.network.etherscan + 'address/' + settings.exchangeAddress
			},
			pairs() {
				return settings.pairs;
			},
			metamask(){
				return this.metamaskAccount == undefined || this.metamaskAccount == "" ? 'metamask-disconect' : 'metamask'
			},
			contract(){
				return this.$parent.contract
			}

		},
		props: {
			from: String,
			pair: Object,
		},
		methods: {
			closeInput(){
				const vm = this;
				vm.newAccount = false;
				vm.incorrectKey = false;
				vm.newAccountKey = '';
			},
			imortKey(){
				const vm = this;
				if (vm.newAccountKey.length > 64) {
					var account = vm.web3.eth.accounts.privateKeyToAccount(vm.newAccountKey);
					if (account.address !== vm.from && account.address !== vm.metamaskAccount) {
						vm.localAccounts.push(account);
						localStorage.setItem('accounts', JSON.stringify(vm.localAccounts))
					}
					vm.newAccountKey = '';
					vm.newAccount = false;
					vm.incorrectKey = false;
					vm.picked = account.address;
				}else{
					vm.incorrectKey = true;
				}
			},
			generateKey(){
				const vm = this;
				if (vm.localAccounts == null) {
					vm.localAccounts = [];
				}
				var account = vm.web3.eth.accounts.create();
				vm.picked = account.address;
				vm.localAccounts.push(account);
				localStorage.setItem('accounts', JSON.stringify(vm.localAccounts))
			},
			deleteWallet(address){
				const vm = this;
				if(address !== vm.from){
					vm.$parent.accounts = vm.localAccounts.filter(function(element) {
						return element.address !== address;
					});
					localStorage.setItem('accounts', JSON.stringify(vm.localAccounts))
				}
			},
			copy(id){
				const vm = this;
				let input = document.getElementById(id)
				input.select()
				try {
					document.execCommand('copy');
					vm.copied = true;

					setTimeout(function(){
						vm.copied = false;
					}, 3000)

				} catch (err) {
					// console.log(err)
				}
				window.getSelection().removeAllRanges()
			},
			
			showMenu(){
				this.menu = this.menu == '' ? 'active' : ''
			},
			showBalance(){
				const vm = this;
				try {
					exchange.balanceOf(vm.contract, vm.pair.tokens[0], vm.from).then(res => {
						vm.amount1 = Number(web3.utils.fromWei(res.toString())).toFixed(6)
					})
					exchange.balanceOf(vm.contract, vm.pair.tokens[1], vm.from).then(res => {
						vm.amount2 = Number(web3.utils.fromWei(res.toString())).toFixed(6)
					})
				} catch(e) {
					console.log(e);
				}
					
			},
			
		},
		watch:{
			pair(){
				this.amount1 = '...'
				this.amount2 = '...'
				this.showBalance();
			},
			from(){
				this.showBalance();
				this.picked = this.from;
			},
			picked(){
				var curAddress = this.picked;
				localStorage.setItem('currentAddress', curAddress);
				this.$parent.from = this.picked;
			}
		},

		created() {
			const vm = this;

			this.$parent.from = this.picked;

			setInterval(function () {
				try {
					vm.showBalance();
				} catch(e) {
					// statements
					console.log(e);
				}
				// vm.checkMetaMask();
			}, 5000)



		}
	}
</script>

<style lang="scss">

	@import '../_base.scss';

	.search-pair{
		outline: none;
		background-color: transparent;
		padding: 5px;
		border: none;
		border-bottom: 1px solid $black-four;
		color: $white;
		width: 100px;

		&::placeholder{
			color: $warm-grey;
		}
	}

	.metamask-toolkit{
		.title{
			text-align: center;
		}
		.extantion-container{
			color: $white;
		}
		a{
			color: $white;
		}
	}

	.input-import{
		display: flex;
		background-color: $black-four;
		padding: 38px 15px 25px;
		position: relative;
		align-items: stretch;
		.input-import__cancel-btn{
			position: absolute;
			top: 15px;
			right: 10px;
			cursor: pointer;
			line-height: 0;
		}
		input.input-import__input{
			box-shadow: none;
			box-sizing: border-box;
			padding: 13px 22px;
			border-radius: 3px;
			background-color: $greyish-brown;
			border: solid 1px $warm-grey;
			&.err{
				outline: 1px solid $grapefruit;
			}
		}
		button.input-import__btn{
			background-color: $algae-green;
			border: 1px solid $algae-green;
			@include Text-Style;
			text-transform: uppercase;
			padding: 13px 21px;
			border-radius: 3px;
		}
	}

	.fade-enter-active, .fade-leave-active {
		transition: opacity .3s;
	}
	.fade-enter, .fade-leave-to /* .fade-leave-active до версии 2.1.8 */ {
		opacity: 0;
	}


	
	.buttuns-container{
		display: flex;
		justify-content: center;
		margin: 15px 0 0;
		.btn{
			border-radius: 3px;
			padding: 8px 21px;
			display: block;
			line-height: 1;
			font-weight: bold;
			border-radius: 3px;
			margin: 0px 5px;
			width: auto;


			&.generate-btn{
				color: $white;
				background-color: $algae-green;
			}

			&.import-btn{
				color: $algae-green;
				border: solid 0.8px $algae-green;
				background-color: transparent;
			}
		}
	}

	.wallets-toolkit{
		padding: 0;
		width: 478px;
		z-index: 5;
	}
	.wallet-container{
		padding: 15px;

		.metamask-img{
			margin: 0 7px;
		}
		&.metamask-container{
			border-top: 22px solid $black-three;



			.wallet_radio label.active{
				background-image: url('../assets/choice-metamask-copy.svg');
				box-shadow: none;
			}

		}
	}
	.wallet-container__item{
		display: flex;
		
		&:not(:first-child){
			margin: 15px 0px;
		}

		.wallet_radio{
			margin-right: 10px;
			input{
				display: none;
			}
			label{
				display: block;
				width: 32px;
				height: 32px;
				background-color: $black-three;
				box-shadow: inset 0 1px 3px 0 rgba(0, 0, 0, 0.5);
				border-radius: 100%;
				cursor: pointer;

				&.active{
					background-image: url('../assets/choice.svg');
					box-shadow: none;
				}
			}
		}

		.input-wallet{
			display: flex;
			position: relative;
			overflow: hidden;

			input{
				display: block;
				box-sizing: border-box;
				width: 306px;
			}

			.input-wallet__private-key{
				position: absolute;
				right: -100%;
			}
		}
	}

	.gasPrice{
		display: flex;
		align-items: center;
		span{
			flex: 3;
		}
		.gasrange{
			flex: 7;
			box-shadow: none;
			display: inline-block;
			padding: 0;
		}
	}
	.toolkit{
		position: absolute;
		right: 0;
		bottom: -5px;
		transform: translateY(100%);
		font-size: 14px;

		&.ledger-toolkit{
			text-align: center;
			padding: 33px 15px;
			line-height: 1.6;
		}
		.title{
			margin-bottom: 16px;
			text-align: center;
		}
		.extantion-container{
			display: flex;
			justify-content: space-between;
			align-items: center;
			padding-bottom: 11px;
			.--padding-left{
				@include Text-Style-11;
			}
			a{
				background-color: $algae-green;
				padding: 8px 13px;
				color: $white;
				border-radius: 2px;
				text-decoration: none;
			}
		}
		.--green{
			color: $algae-green;
		}
		.--purple{
			color: $indigo;
		}
		.indicators{
			display: flex;
			justify-content: space-between;
		}
		.metamask-copy{
			margin-bottom: 14px;
			display: flex;
			justify-content: center;
			align-items: center;
		}
		input{
			font-size: 11px;
			box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.5);
			background-color: $black-three;
			color: $greyish;
			padding: 11px 9px;
			border: none;
			box-sizing: border-box;
			display: block;
			width: 100%;
			outline: none;
		}
		button{
			border: 1px solid $black;
			background-color: $black-three;
			border-radius: none;
			display: block;
			line-height: 0;
			padding: 7px;
			cursor: pointer;
			outline: none;

			&:active{
				box-shadow: inset 0px 1px 3px rgba(0, 0, 0, 0.5);
			}

			img{
				display: block;
				width: 15px;
			}
		}
	}
	.apps__item{
		padding: 7px;
		&.metamask__logo{
			&.disconect{
				filter: grayscale(100%);
			}
		}
		img, i{
			cursor: pointer;
		}
		.toolkit{
			transition: 0.5s ease-in-out;
			z-index: -1;
			opacity: 0;
		}
		&:hover{

			.toolkit{
				z-index: 4;
				opacity: 1;
			}
		}
	}
	.slide-enter-active{
		animation: slide-in .5s;
	}

	.slide-leave-active {
		animation: slide-in .5s reverse;
	}

	@keyframes slide-in{
		0% {
			transform: rotateX(-90deg) translateX(-50%);
		}
		100%{
			transform: rotateX(0deg) translateX(-50%);
		}
	}


	i.ico{
		display: inline-block;
		background-size: cover;
		background-repeat: no-repeat;
		width: 28px;
		height: 25px;
		&.metamask{
			background-image: url(../assets/metaMask.svg);
		}
		&.metamask-disconect{
			background-image: url(../assets/metaMask_disconect.svg)
		}
	}

	.header{
		position: absolute;
		width: 100vw;
		box-sizing: border-box;
		display: flex;
		-ms-align-items: center;
		align-items: center;
		background-color: $black;
		font-size: 14px;
		color: $white;
		height: 46px;
		padding: 0px 23px;
		justify-content: space-between;
	}
	.header__cotainer{
		display: flex;
		-ms-align-items: center;
		align-items: center;
	}
	.header__pairs{
		margin: 0px 36px;
		position: relative;
		font-size: 19px;
	}
	.cur-pair{
		cursor: pointer;
		text-transform: uppercase;
		position: relative;
		padding-right: 20px;

		span{
			position: absolute;
			right: 0;
			top: 50%;
			transform: translateY(-50%);
			line-height: 0;
		}
	}
	.pairs{
		position: absolute;
		list-style-type: none;
		padding: 20px;
		z-index: 2;
		background-color: $black;
		margin: 0;
		transform: translateX(-50%);
		left: 50%;
		transform-origin: 0 0;
	}
	.pair__item{
		margin: 7px 0px;
		a{
			text-transform: uppercase;
			text-decoration: none;
			color: $white;
		}
	}
	.lang-switcher{
		margin: 0px 50px;
		@extend .cur-pair;
	}
	.header__balances{
		display: flex;
	}
	.balances__title{
		text-transform: uppercase;
		color: $greyish;
	}
	.symbol{
		color: $greyish;
	}
	.token-balances-list__item{
		text-transform: uppercase;
		margin: 0px 0px 0px 7px;
	}
	.header__navi{
		display: flex;
		list-style-type: none;
		margin: 0;
		padding: 0;
		margin-right: 50px;
	}
	.header__navi-item{
		a{
			color: $white;
			text-decoration: none;
			text-transform: uppercase;
			margin: 7px;
		}	
		&.--red{
			a{
				color: $grapefruit;
			}
		}
	}
	.apps{
		display: flex;
		-ms-align-items: center;
		align-items: center;
	}
	.menu{
		display: none;
	}



	@media screen and (max-width: 768px) {
		.menu{
			display: block;
			cursor: pointer;
			position: relative;
			z-index: 3;
		}
		.header{
			position: relative;

		}
		.header__logo{
			margin: 10px 0px;
		}
		.header__navi{
			position: absolute;
			flex-direction: column;
			background-color: rgba(0, 0, 0, 0.8);
			padding-top: 60px;
			top: 0;
			left: 100vw;
			height: 100vh;
			z-index: 2;
			text-align: right;

			transition: all 0.4s ease-in-out;

			&.active{
				transform: translateX(-100%);
			}

			.header__navi-item{
				margin: 10px 20px;
			}
		}
		
	}
</style>