import Web3 from 'web3'

export default {
    connectWeb3() {
        if (window.ethereum) {
            window.web3 = new Web3(ethereum);
            try {
                ethereum.enable();
            } catch (error) {
                throw error
            }
        } else if (window.web3) {
            window.web3 = new Web3(web3.currentProvider);
        } else {
            window.web3 = new Web3(new Web3.providers.WebsocketProvider("wss://infura.io/ws"));
        }

        return web3;
    }
}