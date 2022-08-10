import { web3 } from "@/services/connectWeb3";

const convertToWei = (amount) => {
  return web3.utils.toWei(amount.toString());
};

export { convertToWei };
