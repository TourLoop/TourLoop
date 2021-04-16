import { shallow } from 'enzyme';
import Sidebar from '../components/RouteStatistic';
import Navigation from '../components/navigation/Navigation';

describe('<Sidebar />', () => {
  it('renders one <div /> element', () => {
    const wrapper = shallow(<Sidebar />);
    expect(wrapper.find('div')).toHaveLength(1);
  });

  // it('renders one <Navigation /> component', () => {
  //   const wrapper = shallow(<Sidebar />);
  //   expect(wrapper.find(Navigation)).toHaveLength(1);
  // });
});
