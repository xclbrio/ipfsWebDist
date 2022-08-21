import Web3 from 'web3';
import { exchangeAbi, exchangeAddress} from '../settings.json';

const connectWeb3 = () => {
    let web3

    if (ethereum) {
        web3 = new Web3(ethereum);
        try {
            ethereum.enable();
        } catch (error) {
            throw error
        }
    } else if (web3) {
        web3 = new Web3(web3.currentProvider);
    } else {
        web3 = new Web3(new Web3.providers.HttpProvider('https://cloudflare-eth.com/'));
    }

    return web3;
}

const web3 = connectWeb3();
const contract = new web3.eth.Contract(exchangeAbi, exchangeAddress)

export default web3
export {web3, contract}