import { shallow } from 'enzyme';
import Sidebar from '../components/Sidebar';
import Navigation from '../components/navigation/Navigation';
import { render, screen, fireEvent } from '@testing-library/react';
import { defaultPolylines } from '../data/defaultPolylines';

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

  it('populates route legend with checkboxes for each algorithm', () => {
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

    render(
      <Sidebar
        startLocation={{ lat: 53.509905, lng: -113.541233 }}
        endLocation={{ lat: 53.509905, lng: -113.541233 }}
        polylines={newPolylines}
        toggleDisplay={() => {}}
      />
    );

    fireEvent.click(screen.getByText('Legend'));

    expect(screen.getByText('Route Legend')).toBeTruthy();

    const algorithmCheckbox = screen.getByLabelText(
      'Display Route From Algorithm 1'
    );
    fireEvent.click(algorithmCheckbox);

    expect(algorithmCheckbox.checked).toBeTruthy();
  });
});
