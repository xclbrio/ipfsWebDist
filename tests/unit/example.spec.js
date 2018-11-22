import { expect } from 'chai'
import { mount } from '@vue/test-utils'
import app from '@/App.vue'

describe('app.vue', () => {
  it('renders props.msg when passed', () => {
    const msg = 'new message'
    const wrapper = mount(app, {
      propsData: { msg }
    })
    expect(wrapper.text())
  })
})   