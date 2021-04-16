import { shallow } from 'enzyme';
import Header from '../components/Header';
import { render, screen } from '@testing-library/react';

describe('<Header />', () => {
  it('renders one <h1 /> element', () => {
    const wrapper = shallow(<Header />);
    expect(wrapper.find('h1')).toHaveLength(1);
  });

  it('renders with label prop', () => {
    render(<Header label='testLabel' />);
    expect(screen.getByText('testLabel')).toBeTruthy();
  });
});
