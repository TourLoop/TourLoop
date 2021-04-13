import React from 'react';
import PropTypes from 'prop-types';

const Checkbox = props => {
  const { id, style, onChange, checked, label } = props;

  return (
    <div className='flex items-center mb-4'>
      <input
        id={id}
        type='checkbox'
        className='rounded text-indigo-500'
        style={style}
        onChange={onChange}
        checked={checked}
      />
      <label className='ml-2'>{label}</label>
    </div>
  );
};

Checkbox.propTypes = {};

export default Checkbox;
