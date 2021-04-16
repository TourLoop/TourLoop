import { shallow } from 'enzyme';
import NavigationTab from '../../components/navigation/NavigationTab';

describe('<NavigationTab />', () => {
  it('renders one <button /> element', () => {
    const wrapper = shallow(<NavigationTab />);
    expect(wrapper.find('button')).toHaveLength(1);
  });
});
