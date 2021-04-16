import { shallow } from 'enzyme';
import Header from '../components/Header';

describe('<Header />', () => {
  it('renders one <h1 /> element', () => {
    const wrapper = shallow(<Header />);
    expect(wrapper.find('h1')).toHaveLength(1);
  });
});
