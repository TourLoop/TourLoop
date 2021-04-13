import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { decode } from '@googlemaps/polyline-codec';
import Navigation from './navigation/Navigation';
import NavigationTab from './navigation/NavigationTab';
import HelpModal from './HelpModal';
import RouteStatistic from './RouteStatistic';
import useModal from '../hooks/useModal';
import { ReactComponent as HelpIcon } from '../assets/images/help_icon.svg';
import Checkbox from './input/Checkbox';

const algorithms = {
  algo1: 'Algorithm 1',
  algo2: 'Algorithm 2',
  algo3: 'Algorithm 3',
  allBikePaths: 'All Bike Paths',
  allDirtPaths: 'All Dirt Paths',
};

const Sidebar = props => {
  const {
    polylines,
    setPolylines,
    toggleDisplay,
    toggleAllPathsDisplay,
  } = props;
  const [loading, setLoading] = useState(false);
  const [menu, setMenu] = useState('generateRoutes');
  const [dirtPathsChecked, setDirtPathsChecked] = useState(false);
  const [bikePathsChecked, setBikePathsChecked] = useState(false);
  const [pavedPathsChecked, setPavedPathsChecked] = useState(false);
  const [locationChecked, setLocationChecked] = useState(false);
  const [routeStatistics, setRouteStatistics] = useState([]);
  const [errMessage, setErrMessage] = useState('');

  const { isShowing, toggle } = useModal();

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();

  const onSubmit = async data => {
    setLoading(true);
    setErrMessage('');
    const res = await fetch('/api', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });

    if (res.status === 200) {
      const route = await res.json();

      if (route.errMessage) {
        setErrMessage(route.errMessage);
        setLoading(false);
        return;
      }

      const statistics = routeStatistics.filter(
        rs => rs.algorithm !== route.algorithm
      );
      const newRouteStatistics = [
        ...statistics,
        {
          algorithm: route.algorithm,
          distance: route.distance,
          percentPathType: route.percentPathType,
          time: route.time,
        },
      ];

      const latLngs = decode(route.path, 6);
      const paths = latLngs.map(latLng => ({
        lat: latLng[0],
        lng: latLng[1],
      }));

      const newPolylines = polylines.map(polyline =>
        polyline.id === route.algorithm
          ? {
              paths: [paths],
              display: polyline.display,
              id: polyline.id,
              color: polyline.color,
            }
          : polyline
      );

      setPolylines(newPolylines);
      setRouteStatistics(newRouteStatistics);
    } else {
      // error message
    }

    setLoading(false);
  };

  const downloadDatabaseFiles = () => {
    fetch('/export/tar')
      .then(response => response.blob())
      .then(blob => {
        // from https://medium.com/yellowcode/download-api-files-with-react-fetch-393e4dae0d9e
        // 2. Create blob link to download
        const url = window.URL.createObjectURL(new Blob([blob]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'tourloop-database-files.tar.gz');
        // 3. Append to html page
        document.body.appendChild(link);
        // 4. Force download
        link.click();
        // 5. Clean up and remove the link
        link.parentNode.removeChild(link);
      })
      .catch(error => {
        console.log(error);
      });
  };

  return (
    <div
      className='h-screen bg-gray-50 flex flex-col '
      style={{ width: '30vw' }}
    >
      <div className='flex-initial'>
        <div className='flex m-4 mr-4 h-8 justify-between'>
          <h1 className='text-2xl font-medium'>Navigation</h1>
          <div
            className='flex items-center bg-indigo-100 px-3 rounded-full'
            onClick={toggle}
          >
            <span className='mr-2 text-lg text-indigo-500'>Help</span>
            <HelpIcon className='w-6 h-6 text-indigo-500' />
          </div>
        </div>
        <HelpModal isShowing={isShowing} hide={toggle} />
        <Navigation>
          <NavigationTab
            label='Generate'
            onClick={() => setMenu('generateRoutes')}
          />
          <NavigationTab
            label='Legend'
            onClick={() => setMenu('routeLegend')}
          />
          <NavigationTab
            label='Extra'
            onClick={() => setMenu('additionalFunctionality')}
          />
        </Navigation>
      </div>

      {/* <div className='rounded-full bg-gray-500 mx-8 mt-4' style={{ height: '0.01rem'}}></div> */}
      {menu === 'generateRoutes' && (
        <div className='flex-1 '>
          <h1 className='text-center text-2xl mt-2 mb-2 font-medium'>
            Generate Routes
          </h1>
          <form
            onSubmit={handleSubmit(onSubmit)}
            style={{
              display: 'flex',
              flexDirection: 'column',
              paddingLeft: '2rem',
              paddingRight: '2rem',
            }}
            className='flex-1'
          >
            <div className='flex items-center mb-4'>
              <input
                {...register('pointToPoint')}
                id='pointToPoint'
                type='checkbox'
                className='rounded text-indigo-500'
              />
              <label className='ml-2' htmlFor='pointToPoint'>
                Point-to-Point
              </label>
            </div>

            <label htmlFor='startLocation'>Start Location</label>
            <input
              {...register('startLocation', {
                required: true,
              })}
              id='startLocation'
              type='text'
              className='mt-1 mb-4 block w-full rounded-lg border-gray-300 shadow-sm'
            />

            <label htmlFor='endLocation'>End Location</label>
            <input
              {...register('endLocation')}
              id='endLocation'
              type='text'
              className='mt-1 mb-4 block w-full rounded-lg border-gray-300 shadow-sm'
            />

            <label htmlFor='targetRouteDistance'>Target Route Distance</label>
            <input
              {...register('targetRouteDistance', {
                required: true,
                valueAsNumber: true,
              })}
              id='targetRouteDistance'
              type='number'
              className='mt-1 mb-4 block w-full rounded-lg border-gray-300 shadow-sm'
            />

            <label htmlFor='pathType'>Path Type</label>
            <select
              {...register('pathType')}
              id='pathType'
              className='mt-1 mb-4 block w-full rounded-lg border-gray-300 shadow-sm'
            >
              <option value='bike'>Bike Path</option>
              <option value='paved'>Paved Road</option>
              <option value='dirt'>Dirt Trail</option>
            </select>

            <label htmlFor='algorithm'>Algorithm</label>
            <select
              {...register('algorithm')}
              id='algorithm'
              className='mt-1 mb-4 block w-full rounded-lg border-gray-300 shadow-sm'
            >
              <option value='algo1'>Algorithm 1</option>
              <option value='algo2'>Algorithm 2</option>
              <option value='algo3'>Algorithm 3</option>
            </select>

            <button
              type='submit'
              className='mt-1 px-4 py-2 w-48 h-12 bg-indigo-500 shadow-lg rounded-lg font-bold text-white'
              disabled={loading}
              style={{ cursor: loading ? 'not-allowed' : 'pointer' }}
            >
              Generate Routes
            </button>
            {loading && <h2 className='form-submit-header'>Generating...</h2>}
          </form>
          <h3 className='sidebar-err'>{errMessage}</h3>
          <h3 className='sidebar-latlng'>{props.clickedLatLng}</h3>
        </div>
      )}
      {menu === 'routeLegend' && (
        <>
          <h1 className='text-center text-2xl mt-2 mb-2 font-medium'>
            Route Legend
          </h1>
          <div style={{ paddingLeft: '2rem', paddingRight: '2rem' }}>
            {polylines
              .filter(p => p.paths.length > 0)
              .map(p => (
                <Checkbox
                  key={p.id}
                  id={p.id}
                  style={{ color: p.color }}
                  onChange={() => toggleDisplay(p.id)}
                  checked={polylines.find(poly => poly.id === p.id).display}
                  label={`Display Route From ${algorithms[p.id]}`}
                />
              ))}
          </div>
          {routeStatistics.map(rs => (
            <RouteStatistic
              key={rs.algorithm}
              algorithm={algorithms[rs.algorithm]}
              distance={rs.distance}
              percentPathType={rs.percentPathType}
              time={rs.time}
            />
          ))}
        </>
      )}
      {menu === 'additionalFunctionality' && (
        <>
          <h1 className='text-center text-2xl mt-2 mb-2 font-medium'>
            Additional Functionality
          </h1>
          <div
            style={{
              display: 'flex',
              flexDirection: 'column',
              paddingLeft: '2rem',
              paddingRight: '2rem',
            }}
          >
            <Checkbox
              id='allDirtPaths'
              onChange={() => {
                setDirtPathsChecked(!dirtPathsChecked);
                toggleAllPathsDisplay('allDirtPaths', '/api/alldirtpaths');
              }}
              checked={dirtPathsChecked}
              label='Display All Dirt Paths'
            />
            <Checkbox
              id='allBikePaths'
              onChange={() => {
                setBikePathsChecked(!bikePathsChecked);
                toggleAllPathsDisplay('allBikePaths', '/api/allbikepaths');
              }}
              checked={bikePathsChecked}
              label='Display All Bike Paths'
            />
            <Checkbox
              id='allPavedPaths'
              onChange={() => {
                setPavedPathsChecked(!pavedPathsChecked);
                toggleAllPathsDisplay('allPavedPaths', '/api/allpavedpaths');
              }}
              checked={pavedPathsChecked}
              label='Display All Paved Paths'
            />
            <Checkbox
              id='locationToggle'
              onChange={() => {
                setLocationChecked(!locationChecked);
                props.setUseLocation(!props.useLocation);
              }}
              checked={locationChecked}
              label='Track Current Location'
            />
            <button className='button' onClick={downloadDatabaseFiles}>
              Download Database
            </button>
          </div>
        </>
      )}
    </div>
  );
};

export default Sidebar;
