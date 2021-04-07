import React from 'react';
import PropTypes from 'prop-types';

const NavigationTab = props => {
  const { label, onClick } = props;
  return (
    <button className='navigation-tab' onClick={onClick}>
      {label}
    </button>
  );
};

NavigationTab.propTypes = {};

export default NavigationTab;
