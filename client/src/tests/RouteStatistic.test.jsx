import { shallow } from 'enzyme';
import RouteStatistic from '../components/RouteStatistic';

describe('<RouteStatistic />', () => {
  it('renders one <div /> element', () => {
    const wrapper = shallow(<RouteStatistic />);
    expect(wrapper.find('div')).toHaveLength(1);
  });

  it('renders ', () => {
    const wrapper = shallow(
      <RouteStatistic
        algorithm='Algorithm 1'
        distance={5.6789}
        percentPathType={42}
        time={1.2345}
      />
    );

    expect(wrapper.find('div')).toHaveLength(1);
  });
});
