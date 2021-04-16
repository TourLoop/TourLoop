import { shallow } from 'enzyme';
import Map from '../components/Map';
import { GoogleMap } from '@react-google-maps/api';
import { defaultPolylines } from '../data/defaultPolylines';

describe('<Map />', () => {
  it('renders one <GoogleMap /> component', () => {
    const wrapper = shallow(<Map polylines={[]} />);
    expect(wrapper.find(GoogleMap)).toHaveLength(1);
  });

  it('renders polylines with at least one non-empty path in polylines prop', () => {
    const polylines = defaultPolylines.filter(p => p.id !== 'algo1');
    const newPolylines = [
      ...polylines,
      {
        paths: [[53.509905, -113.541233]],
        display: true,
        id: 'algo1',
        color: '#FF6347',
      },
    ];
    const wrapper = shallow(<Map polylines={newPolylines} />);

    expect(wrapper.find(GoogleMap)).toHaveLength(1);
  });
});
