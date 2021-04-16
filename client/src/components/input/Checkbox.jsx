import React from 'react';
import PropTypes from 'prop-types';

const Checkbox = props => {
  const { id, style, onChange, checked, label } = props;

  return (
    <div className='checkbox'>
      <input
        id={id}
        type='checkbox'
        className='checkbox-input'
        style={style}
        onChange={onChange}
        checked={checked}
      />
      <label htmlFor={id} className='checkbox-label'>
        {label}
      </label>
    </div>
  );
};

Checkbox.propTypes = {};

export default Checkbox;
