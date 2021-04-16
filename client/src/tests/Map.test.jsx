import { shallow } from 'enzyme';
import Map from '../components/Map';
import { GoogleMap } from '@react-google-maps/api';

describe('<Map />', () => {
  it('renders one <GoogleMap /> component', () => {
    const wrapper = shallow(<Map polylines={[]} />);
    expect(wrapper.find(GoogleMap)).toHaveLength(1);
  });
});
