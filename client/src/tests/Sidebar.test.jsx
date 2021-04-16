import { shallow } from 'enzyme';
import Sidebar from '../components/Sidebar';
import Navigation from '../components/navigation/Navigation';
import { render, screen, fireEvent } from '@testing-library/react';

describe('<Sidebar />', () => {
  it('renders one <Navigation /> component', () => {
    const wrapper = shallow(<Sidebar />);
    expect(wrapper.find(Navigation)).toHaveLength(1);
  });

  it('changes start & end location input values on render', () => {
    render(
      <Sidebar
        startLocation={{ lat: 53.509905, lng: -113.541233 }}
        endLocation={{ lat: 53.509905, lng: -113.541233 }}
        pointToPointChecked
      />
    );

    const startLocationInput = screen.getByLabelText('Start Location');
    const endLocationInput = screen.getByLabelText('End Location');

    expect(startLocationInput.value).toBe('53.509905, -113.541233');

    expect(endLocationInput.value).toBe('53.509905, -113.541233');
  });

  it('changes start & end location input values on blur', () => {
    render(
      <Sidebar
        startLocation={{ lat: 53.509905, lng: -113.541233 }}
        endLocation={{ lat: 53.509905, lng: -113.541233 }}
        setStartLocation={() => {}}
        setEndLocation={() => {}}
        pointToPointChecked
      />
    );

    const startLocationInput = screen.getByLabelText('Start Location');
    const endLocationInput = screen.getByLabelText('End Location');

    startLocationInput.focus();
    startLocationInput.blur();
    endLocationInput.focus();
    endLocationInput.blur();

    expect(startLocationInput.value).toBe('53.509905, -113.541233');
    expect(endLocationInput.value).toBe('53.509905, -113.541233');
  });
});
