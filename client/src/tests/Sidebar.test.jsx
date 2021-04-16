import { shallow } from 'enzyme';
import Sidebar from '../components/Sidebar';
import Navigation from '../components/navigation/Navigation';
import { render, screen } from '@testing-library/react';

describe('<Sidebar />', () => {
  it('renders one <Navigation /> component', () => {
    const wrapper = shallow(<Sidebar />);
    expect(wrapper.find(Navigation)).toHaveLength(1);
  });

  it('changes start & end location input values', () => {
    render(
      <Sidebar
        startLocation={{ lat: 53.509905, lng: -113.541233 }}
        endLocation={{ lat: 53.509905, lng: -113.541233 }}
      />
    );

    const startLocationInput = screen.getByLabelText('Start Location');
    const endLocationInput = screen.getByLabelText('Start Location');

    expect(startLocationInput.value).toBe('53.509905, -113.541233');
    expect(endLocationInput.value).toBe('53.509905, -113.541233');
  });
});
