import { shallow } from 'enzyme';
import HelpModal from '../components/HelpModal';

describe('<HelpModal />', () => {
  it('renders six <div /> elements', () => {
    const wrapper = shallow(<HelpModal isShowing />);
    expect(wrapper.find('div')).toHaveLength(6);
  });
});
