import { expect } from 'chai'
import { mount} from '@vue/test-utils'
// // import workflow from '@/components/workflow.vue'

import Web3 from 'web3'

const web3 = new Web3(new Web3.providers.HttpProvider("https://kovan.infura.io"));



// // describe('workflow', () => {
// // 	it('connect web3', () => {
// // 		const wrapper = mount(workflow);

// // 		wrapper.setData({
// // 			web3: web3
// // 		})
// // 	})
// // })


console.log(web3);