import React from 'react';
import PropTypes from 'prop-types';

const Navigation = props => {
  const { children } = props;

  return <div className='navigation'>{children}</div>;
};

Navigation.propTypes = {};

export default Navigation;
