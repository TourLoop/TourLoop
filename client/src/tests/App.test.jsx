import { shallow } from 'enzyme';
import App from '../components/App';
import Map from '../components/Map.jsx';
import Sidebar from '../components/Sidebar.jsx';
import { render, screen, fireEvent } from '@testing-library/react';

describe('<App />', () => {
  it('renders one <Map /> component', () => {
    const wrapper = shallow(<App />);
    expect(wrapper.find(Map)).toHaveLength(1);
  });

  it('renders one <Sidebar /> component', () => {
    const wrapper = shallow(<App />);
    expect(wrapper.find(Sidebar)).toHaveLength(1);
  });

  it('changes start location input', () => {
    render(<App />);
    const startLocationInput = screen.getByLabelText('startLocation');

    fireEvent.change(startLocationInput, {
      target: { value: '53.509905, -113.541233' },
    });
    expect(startLocationInput.value).toBe('53.509905, -113.541233');
  });
});
