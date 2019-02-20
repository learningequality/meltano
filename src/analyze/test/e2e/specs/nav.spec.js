import { shallowMount } from '@vue/test-utils';
import MainNav from '@/components/MainNav.vue';

describe('MainNav.vue', () => {
  it('renders props.msg when passed', () => {
    const msg:String = 'new message';
    const wrapper = shallowMount(MainNav);
    // expect(wrapper.text()).toMatch(msg);
    console.log(wrapper);
  });
});
