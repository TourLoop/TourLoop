import { shallow } from 'enzyme';
import Checkbox from '../../components/input/Checkbox';

describe('<Checkbox />', () => {
  it('renders one <div /> element', () => {
    const wrapper = shallow(<Checkbox />);
    expect(wrapper.find('div')).toHaveLength(1);
  });
});
