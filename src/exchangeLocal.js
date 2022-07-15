export default {
	signAndSend(tx_, contractFunction_, functionAbi_, contractAddress_, account_, pkey_, gasPrice_, value_, getHash, callback) {
		let estimatedGas;
		let nonce;

		contractFunction_.estimateGas({ from: account_ }).then((gasAmount) => {
			estimatedGas = gasAmount.toString(16);

			console.log("Estimated gas: " + estimatedGas);

			web3.eth.getTransactionCount(account_).then(_nonce => {
				nonce = _nonce.toString(16);

				console.log("Nonce: " + nonce);
				const txParams = {
					gasPrice: gasPrice_,
					gasLimit: 3000000,
					to: contractAddress_,
					data: functionAbi_,
					from: account_,
					nonce: '0x' + nonce,
					value: value_,
				};

				const tx = new tx_(txParams);

				
				tx.sign(pkey_); // Transaction Signing here

				const serializedTx = tx.serialize();

				web3.eth.sendSignedTransaction('0x' + serializedTx.toString('hex')).once('transactionHash', function(hash){ 
					getHash(hash)
					console.log(hash);
				}).then(receipt => {
					callback(receipt);
				}).catch(err => console.log(err));
			});
		});
	},
	depositLocal(web3_, tx_, exchangeContract_, exchangeAddress_, account_, pkey_, gasPrice_, value_, getHash) {
		 
		const depositFunction = exchangeContract_.methods.deposit();
		const depositAbi = depositFunction.encodeABI();
		this.signAndSend(tx_, depositFunction, depositAbi, exchangeAddress_, account_, pkey_, gasPrice_, value_, getHash);
	},
	withdrawLocal(web3_, tx_, exchangeContract_, exchangeAddress_, account_, pkey_, gasPrice_, amount_, value_, getHash) {
		 
		const withdrawFunction = exchangeContract_.methods.withdraw(amount_);
		const withdrawAbi = withdrawFunction.encodeABI();
		this.signAndSend(tx_, withdrawFunction, withdrawAbi, exchangeAddress_, account_, pkey_, gasPrice_, value_, getHash);
	},
	depositTokenLocal(web3_, tx_, exchangeContract_, tokenContract_, exchangeAddress_, tokenAddress_, account_, pkey_, gasPrice_, amount_, value_, getHash) {
		 
		const approveFunction = tokenContract_.methods.approve(exchangeAddress_, amount_);
		const approveAbi = approveFunction.encodeABI();
		const depositFunction = exchangeContract_.methods.depositToken(tokenAddress_, amount_);
		const depositAbi = depositFunction.encodeABI();
		this.signAndSend(tx_, approveFunction, approveAbi, tokenAddress_, account_, pkey_, gasPrice_, value_, getHash, function(res){
			console.log(res);
			this.signAndSend(tx_, depositFunction, depositAbi, exchangeAddress_, account_, pkey_, gasPrice_, value_, getHash, res => console.log(res));
		});
	},
	withdrawTokenLocal(web3_, tx_, exchangeContract_, tokenContract_, exchangeAddress_, tokenAddress_, account_, pkey_, gasPrice_, amount_, value_, getHash) {
		 
		const withdrawFunction = exchangeContract_.methods.withdrawToken(tokenAddress_, amount_);
		const withdrawAbi = withdrawFunction.encodeABI();
		this.signAndSend(tx_, withdrawFunction, withdrawAbi, exchangeAddress_, account_, pkey_, gasPrice_, value_, getHash, res => console.log(res));
	},
	trade(exchangeContract_, tx_, exchangeAddress_, account_, pkey_, gasPrice_, value_, tokenGet_, amountGet_, tokenGive_, amountGive_, expires_, nonce_, user_, v_, r_, s_, amount_, pair_, gethash){
		 
		const tradeFunction = exchangeContract_.methods.trade(tokenGet_, amountGet_, tokenGive_, amountGive_, expires_, nonce_, user_, v_, r_, s_, amount_, pair_);
		const tradeAbi = tradeFunction.encodeABI();

		console.log(tradeFunction)
		this.signAndSend(tx_, tradeFunction, tradeAbi, exchangeAddress_, account_, pkey_, gasPrice_, value_, gethash, function(res){
			console.log(res);
		});
	},
	cancel(exchangeContract_, tx_, exchangeAddress_, account_, pkey_, gasPrice_, value_, tokenGet_, amountGet_, tokenGive_, amountGive_, expires_, nonce_, v_, r_, s_, pair, callback){
		 
		const cancelFunction = exchangeContract_.methods.cancelOrder(tokenGet_, amountGet_, tokenGive_, amountGive_, expires_, nonce_, v_, r_, s_, pair);
		const cancelAbi = cancelFunction.encodeABI();
		this.signAndSend(tx_, cancelFunction, cancelAbi, exchangeAddress_, account_, pkey_, gasPrice_, value_, callback);
	},
}