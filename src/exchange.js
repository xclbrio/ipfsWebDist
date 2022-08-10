/*
*
v0.0.1 Exhange smart contract methods.
SETUP
<script src="js/exchange.js"></script>
var web3 = connectWeb3(provider_); //import `provider_` from `./settings`
var from = getAccount(0)
var contract = initContract(abi, contractAddress) //import `abi` and `contractAddress` from `./settings`
*
*/

import { web3, contract } from "./services/connectWeb3";

export default {
  // connectWeb3: function (provider_) {
  //   if (typeof web3 !== "undefined") {
  //     return new Web3(Web3.currentProvider);
  //   } else {
  //     return new Web3(new Web3.providers.HttpProvider(provider_));
  //   }
  // },
  // connectWebsocketWeb3: function (provider_) {
  //   return new Web3(new Web3.providers.WebsocketProvider(provider_));
  // },
  initContract: function (abi_, contractAddress_) {
    return new web3.eth.Contract(abi_, contractAddress_);
  },
  getAccount: async function (accountIndex_) {
    const account = await web3.eth.getAccounts();
    return account[accountIndex_];
  },

  deposit: async function (contract_, from_, amount_, callback) {
    let str;
    await contract_.methods
      .deposit()
      .send({ from: from_, value: amount_ }, function (err, hash) {
        if (!err) {
          str = hash;
          callback(hash);
          // alert(`https://kovan.etherscan.io/tx/${hash}`);
        } else {
          // alert(err);
        }
      });

    return await str;
  },
  withdraw: async function (contract_, from_, amount_, callback) {
    let str;
    await contract_.methods
      .withdraw(amount_)
      .send({ from: from_ }, function (err, hash) {
        if (!err) {
          str = hash;
          // alert(`https://kovan.etherscan.io/tx/${hash}`);
        } else {
          // alert(err);
        }
        callback(hash);
      });
    return await str;
  },
  depositToken: async function (
    contract_,
    tokenContract_,
    from_,
    spender_,
    token_,
    amount_,
    callback
  ) {
    let str;
    await tokenContract_.methods
      .approve(spender_, amount_)
      .send({ from: from_ }, function (err, hash) {
        if (!err) {
          str = hash;
          // alert(`https://kovan.etherscan.io/tx/${hash}`);
        } else {
          // alert(err);
        }
        callback(hash);

        // slyapa

        var checkTransaction = setInterval(() => {
          web3.eth.getTransactionReceipt(hash).then((res) => {
            console.log(res.blockNumber);
            if (res.blockNumber !== null) {
              clearInterval(checkTransaction);
              contract_.methods
                .depositToken(token_, amount_)
                .send({ from: from_ }, function (err, hash) {
                  if (!err) {
                    str = hash;
                  } else {
                    console.log(err);
                  }
                  callback(hash);
                });
            }
          });
        }, 3000);

        // slyapa end
      });

    // here is plan b

    // await contract_.methods.depositToken(token_, amount_).send({from:from_},
    // 	function(err, hash){
    // 		if (!err){
    // 			// alert(`https://kovan.etherscan.io/tx/${hash}`);
    // 			str = hash;
    // 		} else {
    // 			// alert(err);
    // 		}
    // 		callback(hash);
    // });

    return await str;
  },
  withdrawToken: async function (contract_, from_, token_, amount_, callback) {
    let str;
    await contract_.methods
      .withdrawToken(token_, amount_)
      .send({ from: from_ }, function (err, hash) {
        if (!err) {
          // alert(`https://kovan.etherscan.io/tx/${hash}`);
          str = hash;
        } else {
          // alert(err);
        }
        callback(hash);
      });
    return await str;
  },
  balanceOf: async function (token_, user_) {
    return await contract.methods.balanceOf(token_, user_).call();
  },
  order: async function (
    contract_,
    from_,
    tokenGet_,
    amountGet_,
    tokenGive_,
    amountGive_,
    expires_,
    nonce_
  ) {
    let str;
    await contract_.methods
      .order(tokenGet_, amountGet_, tokenGive_, amountGive_, expires_, nonce_)
      .send({ from: from_ }, function (err, hash) {
        if (!err) {
          str = hash;
          // alert(`https://kovan.etherscan.io/tx/${hash}`);
        } else {
          // alert(err);
        }
      });
    return await str;
  },
  // offchainOrder: function (contract_, from_, contract_, tokenGet, amountGet, tokenGive, amountGive, expires, nonce) {
  // 	// var hash = rderHash(contract_, tokenGet, amountGet, tokenGive, amountGive, expires, nonce);
  // 	// var sig = sign(from_, hash);
  // },
  trade: async function (
    contract_,
    from_,
    tokenGet_,
    amountGet_,
    tokenGive_,
    amountGive_,
    expires_,
    nonce_,
    user_,
    v_,
    r_,
    s_,
    amount_,
    pair_,
    callback
  ) {
    let str;
    console.log([
      tokenGet_,
      amountGet_,
      tokenGive_,
      amountGive_,
      expires_,
      nonce_,
      user_,
      v_,
      r_,
      s_,
      amount_,
      pair_,
    ]);
    await contract_.methods
      .trade(
        tokenGet_,
        amountGet_,
        tokenGive_,
        amountGive_,
        expires_,
        nonce_,
        user_,
        v_,
        r_,
        s_,
        amount_,
        pair_
      )
      .send({ from: from_ }, function (err, hash) {
        if (!err) {
          // hashInput_ = String(hash);
          str = hash;
          console.log(hash);
          // alert(`https://kovan.etherscan.io/tx/${hash}`);
        } else {
          // alert(err);
          // alert('not ok')
        }

        callback(hash);
      });
    return await str;
  },
  rsv: function (sig_) {
    const sig = sig_.slice(2);
    const r = "0x" + sig.slice(0, 64);
    const s = "0x" + sig.slice(64, 128);
    const v = web3.utils.toDecimal("0x" + sig.slice(128, 130));
    return { r, s, v };
  },
  cancelOrder: async function (
    contract_,
    from_,
    tokenGet_,
    amountGet_,
    tokenGive_,
    amountGive_,
    expires_,
    nonce_,
    v_,
    r_,
    s_,
    pair,
    callback
  ) {
    let str;
    await contract_.methods
      .cancelOrder(
        tokenGet_,
        amountGet_,
        tokenGive_,
        amountGive_,
        expires_,
        nonce_,
        v_,
        r_,
        s_,
        pair
      )
      .send({ from: from_ }, function (err, hash) {
        if (!err) {
          str = hash;
          // alert(`https://kovan.etherscan.io/tx/${hash}`);
        } else {
          // alert(err);
        }
        callback(hash);
      });
    return await str;
  },
  sign(from_, hash_) {
    return web3.eth.personal.sign(hash_, from_);
  },

  async checkSig(hash_, sig_) {
    return await web3.eth.personal.ecRecover(hash_, sig_);
  },
  orderHash(tokenGet_, tokenGive_, amountGet_, amountGive_, expires_, nonce_) {
    return web3.utils.soliditySha3(
      tokenGet_,
      amountGet_,
      tokenGive_,
      amountGive_,
      expires_,
      nonce_
    );
  },
  async getSign(
    from_,
    privateKey_,
    tokenGet_,
    tokenGive_,
    amountGet_,
    amountGive_,
    expires_
  ) {
    const nonce = Math.floor(Math.random() * 1000000) + 100;
    const hash = this.orderHash(
      amountGet_,
      amountGive_,
      tokenGet_,
      tokenGive_,
      expires_,
      nonce
    );
    const sign = privateKey_
      ? web3.eth.accounts.sign(hash, privateKey_).signature
      : await this.sign(from_, hash);
    return { hash, sign, nonce };
  },

  approve: async function (from_, spender_, value_) {
    let str;
    await contract.methods
      .approve(spender_, value_)
      .send({ from: from_ }, function (err, hash) {
        if (!err) {
          str = hash;
          // alert(`https://kovan.etherscan.io/tx/${hash}`);
        } else {
          // alert(err);
        }
      });
    return await str;
  },
  transferFrom: async function (contract_, from_, _from, to_, value_) {
    let str;
    await contract_.methods
      .transferFrom(_from, to_, value_)
      .send({ from: from_ }, function (err, hash) {
        if (!err) {
          str = hash;
          // alert(`https://kovan.etherscan.io/tx/${hash}`);
        } else {
          // alert(err);
        }
      });
    return await str;
  },
  orderEvent: async function (contract_) {
    let str;
    await contract_.events.Order({ fromBlock: 0 }, function (error, event) {
      if (!error) {
        str = event;
        // alert(event.transactionHash);
        // alert('==============');
      } else {
        // alert(error);
      }
    });
    return await str;
  },
};
