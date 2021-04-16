import React from 'react';
import PropTypes from 'prop-types';

const RouteStatistic = props => {
  const { algorithm, distance, percentPathType, time } = props;

  return (
    <div className='route-statistic'>
      <h2 className='route-statistic-header'>
        Algorithm: <span>{algorithm}</span>
      </h2>
      <h2 className='route-statistic-header'>
        Distance: <span>{distance ? distance.toFixed(3) : ''} km</span>
      </h2>
      {/* <h2 className='route-statistic-header'>
        Percent Path Type: <span>{percentPathType}%</span>
      </h2> */}
      <h2 className='route-statistic-header'>
        Time: <span>{time ? time.toFixed(3) : ''} seconds</span>
      </h2>
    </div>
  );
};

RouteStatistic.propTypes = {};

export default RouteStatistic;
