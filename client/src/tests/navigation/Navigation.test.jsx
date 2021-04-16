import { shallow } from 'enzyme';
import Navigation from '../../components/navigation/Navigation';

describe('<Navigation />', () => {
  it('renders one <div /> element', () => {
    const wrapper = shallow(<Navigation />);
    expect(wrapper.find('div')).toHaveLength(1);
  });
});
