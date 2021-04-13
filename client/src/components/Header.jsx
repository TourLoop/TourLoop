import React from 'react';
import PropTypes from 'prop-types';

const Header = props => {
  const { label } = props;

  return <h1 className='header'>{label}</h1>;
};

Header.propTypes = {};

export default Header;
