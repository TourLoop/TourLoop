import { shallow } from 'enzyme';
import RouteStatistic from '../components/RouteStatistic';

describe('<RouteStatistic />', () => {
  it('renders one <div /> element', () => {
    const wrapper = shallow(<RouteStatistic />);
    expect(wrapper.find('div')).toHaveLength(1);
  });
});
