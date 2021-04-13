import React from 'react';
import PropTypes from 'prop-types';

const NavigationTab = props => {
  const { label, onClick } = props;
  return (
    <button
      className='flex-1 mx-2 h-12 bg-indigo-500 shadow-lg rounded-lg  font-bold text-white text-sm'
      onClick={onClick}
    >
      {label}
    </button>
  );
};

NavigationTab.propTypes = {};

export default NavigationTab;
