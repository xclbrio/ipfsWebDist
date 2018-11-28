import { expect } from 'chai'
import { mount, createLocalVue } from '@vue/test-utils'
import VueRouter from 'vue-router'
import app from '@/App.vue'

const localVue = createLocalVue()
localVue.use(VueRouter)
const router = new VueRouter()


describe('app.vue', () => {
  it('renders props.msg when passed', () => {
    const wrapper = mount(app, {
		localVue,
		router
    })
    expect(wrapper.text())
  })
})   