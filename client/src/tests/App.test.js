import { shallow } from 'enzyme';
import App from '../components/App';
import Map from '../components/Map.jsx';
import Sidebar from '../components/Sidebar.jsx';

describe('<App />', () => {
  it('renders one <Map /> component', () => {
    const wrapper = shallow(<App />);
    expect(wrapper.find(Map)).toHaveLength(1);
  });

  it('renders one <Sidebar /> component', () => {
    const wrapper = shallow(<App />);
    expect(wrapper.find(Sidebar)).toHaveLength(1);
  });
});
