import React from 'react';
import PropTypes from 'prop-types';

const Navigation = props => {
  const { children } = props;

  return <div className='px-2 py-1 flex'>{children}</div>;
};

Navigation.propTypes = {};

export default Navigation;
