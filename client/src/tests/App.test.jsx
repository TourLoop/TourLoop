import { shallow } from 'enzyme';
import App from '../components/App';
import Map from '../components/Map';
import Sidebar from '../components/Sidebar';
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
    const startLocationInput = screen.getByLabelText('Start Location');
    const targetDistanceInput = screen.getByLabelText('Target Route Distance');

    fireEvent.change(startLocationInput, {
      target: { value: '53.509905, -113.541233' },
    });

    fireEvent.change(targetDistanceInput, {
      target: { value: '3' },
    });

    expect(startLocationInput.value).toBe('53.509905, -113.541233');
    expect(targetDistanceInput.value).toBe('3');

    // const generateRoutesButton = screen.getByLabelText('generateRoutes');
    // fireEvent.click(generateRoutesButton);
  });

  it('clicks on "Generate" navigation button', () => {
    render(<App />);

    fireEvent.click(screen.getByText('Generate'));

    expect(screen.getByText('Generate Routes')).toBeTruthy();
  });

  it('clicks on "Legend" navigation button', () => {
    render(<App />);

    fireEvent.click(screen.getByText('Legend'));

    expect(screen.getByText('Route Legend')).toBeTruthy();
  });

  it('clicks on "Extra" navigation button', () => {
    render(<App />);

    fireEvent.click(screen.getByText('Extra'));

    expect(screen.getByText('Additional Functionality')).toBeTruthy();
  });

  it('clicks on "Point-to-Point" checkbox', () => {
    render(<App />);

    const pointToPoint = screen.getByLabelText('Point-to-Point');
    fireEvent.click(pointToPoint);

    expect(pointToPoint.checked).toBeTruthy();
  });

  it('clicks on "Display All Dirt Paths" checkbox', () => {
    render(<App />);

    fireEvent.click(screen.getByText('Extra'));

    expect(screen.getByText('Additional Functionality')).toBeTruthy();

    const allDirtPaths = screen.getByLabelText('Display All Dirt Paths');
    fireEvent.click(allDirtPaths);

    expect(allDirtPaths.checked).toBeTruthy();
  });

  it('clicks on "Display All Bike Paths" checkbox', () => {
    render(<App />);

    fireEvent.click(screen.getByText('Extra'));

    expect(screen.getByText('Additional Functionality')).toBeTruthy();

    const allBikePaths = screen.getByLabelText('Display All Bike Paths');
    fireEvent.click(allBikePaths);

    expect(allBikePaths.checked).toBeTruthy();
  });

  it('clicks on "Track Current Location" checkbox', () => {
    render(<App />);

    fireEvent.click(screen.getByText('Extra'));

    expect(screen.getByText('Additional Functionality')).toBeTruthy();

    const currentLocation = screen.getByLabelText('Track Current Location');
    fireEvent.click(currentLocation);

    expect(currentLocation.checked).toBeTruthy();
  });

  it('clicks on "Download Database" button', () => {
    render(<App />);

    fireEvent.click(screen.getByText('Extra'));

    expect(screen.getByText('Additional Functionality')).toBeTruthy();

    const downloadDatabase = screen.getByLabelText('downloadDatabase');
    fireEvent.click(downloadDatabase);
  });
});
