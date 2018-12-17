const Web3 = require('web3');
const web3 = new Web3(new Web3.providers.HttpProvider("http://kovan.infura.io/"));


web3.eth.getBalance('0x3e9227057494996A0B51a3a6AB91319025F0edd1').then(res => {
	console.log(res)
})

// module.exports = web3;
