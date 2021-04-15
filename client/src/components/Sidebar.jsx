import { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { decode } from '@googlemaps/polyline-codec';
import Navigation from './navigation/Navigation';
import NavigationTab from './navigation/NavigationTab';
import HelpModal from './HelpModal';
import RouteStatistic from './RouteStatistic';
import useModal from '../hooks/useModal';
import { ReactComponent as HelpIcon } from '../assets/images/help_icon.svg';
import Checkbox from './input/Checkbox';
import Header from './Header';

const algorithms = {
  algo1: 'Algorithm 1',
  algo2: 'Algorithm 2',
  algo3: 'Algorithm 3',
  allBikePaths: 'All Bike Paths',
  allDirtPaths: 'All Dirt Paths',
  allPavedPaths: 'All Paved Paths',
};

const Sidebar = (props) => {
  const {
    polylines,
    setPolylines,
    toggleDisplay,
    toggleAllPathsDisplay,
    pointToPointChecked,
    setPointToPointChecked,
    startLocation,
    setStartLocation,
    endLocation,
    setEndLocation,
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
    setValue,
  } = useForm();

  useEffect(() => {
    if (startLocation.lat && startLocation.lng) {
      setValue('startLocation', `${startLocation.lat}, ${startLocation.lng}`);
    } else {
      setValue('startLocation', '');
    }
  }, [startLocation]);

  useEffect(() => {
    if (endLocation.lat && endLocation.lng) {
      setValue('endLocation', `${endLocation.lat}, ${endLocation.lng}`);
    } else {
      setValue('endLocation', '');
    }
  }, [endLocation]);

  const handleStartLocation = (e) => {
    const latLng = e.target.value.split(',');
    const coord =
      +latLng[0] && +latLng[1]
        ? {
            lat: +latLng[0],
            lng: +latLng[1],
          }
        : {
            lat: 0,
            lng: 0,
          };
    setStartLocation(coord);
  };

  const handleEndLocation = (e) => {
    const latLng = e.target.value.split(',');
    const coord =
      +latLng[0] && +latLng[1]
        ? {
            lat: +latLng[0],
            lng: +latLng[1],
          }
        : {
            lat: 0,
            lng: 0,
          };
    setEndLocation(coord);
  };

  const onSubmit = async (data) => {
    setLoading(true);

    if (!pointToPointChecked) {
      data.endLocation = data.startLocation;
    }

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
        (rs) => rs.algorithm !== route.algorithm
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
      const paths = latLngs.map((latLng) => ({
        lat: latLng[0],
        lng: latLng[1],
      }));

      const newPolylines = polylines.map((polyline) =>
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
      .then((response) => response.blob())
      .then((blob) => {
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
      .catch((error) => {
        console.log(error);
      });
  };

  return (
    <div className='sidebar'>
      <div className='flex-initial'>
        <div className='flex m-4 mr-4 h-8 justify-between'>
          <h1 className='navigation-header'>Navigation</h1>
          <div className='help-wrapper' onClick={toggle}>
            <span className='help-label'>Help</span>
            <HelpIcon className='help-icon' />
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
      {menu === 'generateRoutes' && (
        <div className='flex-1'>
          <Header label='Generate Routes' />
          <form onSubmit={handleSubmit(onSubmit)} className='px-8'>
            <div className='flex items-center mb-4'>
              <input
                {...register('pointToPoint')}
                id='pointToPoint'
                type='checkbox'
                className='rounded text-indigo-500'
                onChange={() => setPointToPointChecked(!pointToPointChecked)}
                checked={pointToPointChecked}
              />
              <label className='ml-2' htmlFor='pointToPoint'>
                Point-to-Point
              </label>
            </div>

            <label htmlFor='startLocation'>Start Location</label>
            <input
              {...register('startLocation')}
              id='startLocation'
              type='text'
              className='input'
              onBlur={handleStartLocation}
            />

            {pointToPointChecked && (
              <>
                <label htmlFor='endLocation'>End Location</label>
                <input
                  {...register('endLocation')}
                  id='endLocation'
                  type='text'
                  className='input'
                  onBlur={handleEndLocation}
                />
              </>
            )}

            <label htmlFor='targetRouteDistance'>Target Route Distance</label>
            <input
              {...register('targetRouteDistance', {
                required: true,
                valueAsNumber: true,
              })}
              id='targetRouteDistance'
              type='number'
              step='0.001'
              className='input'
            />

            <label htmlFor='pathType'>Path Type</label>
            <select {...register('pathType')} id='pathType' className='input'>
              <option value='bike'>Bike Path</option>
              <option value='paved'>Paved Road</option>
              <option value='dirt'>Dirt Trail</option>
            </select>

            <label htmlFor='algorithm'>Algorithm</label>
            <select {...register('algorithm')} id='algorithm' className='input'>
              <option value='algo1'>Algorithm 1</option>
              <option value='algo2'>Algorithm 2</option>
              <option value='algo3'>Algorithm 3</option>
            </select>

            <button
              type='submit'
              className='button'
              disabled={loading}
              style={{ cursor: loading ? 'not-allowed' : 'pointer' }}
            >
              Generate Routes
            </button>
            {loading && <h2 className='form-submit-header'>Generating...</h2>}
          </form>
          <h3 className='sidebar-err'>{errMessage}</h3>
        </div>
      )}
      {menu === 'routeLegend' && (
        <div className='flex-1'>
          <Header label='Route Legend' />
          <div className='px-8'>
            {polylines
              .filter((p) => p.paths.length > 0)
              .map((p) => (
                <Checkbox
                  key={p.id}
                  id={p.id}
                  style={{ color: p.color }}
                  onChange={() => toggleDisplay(p.id)}
                  checked={polylines.find((poly) => poly.id === p.id).display}
                  label={`Display Route From ${algorithms[p.id]}`}
                />
              ))}
          </div>
          {routeStatistics.map((rs) => (
            <RouteStatistic
              key={rs.algorithm}
              algorithm={algorithms[rs.algorithm]}
              distance={rs.distance}
              percentPathType={rs.percentPathType}
              time={rs.time}
            />
          ))}
        </div>
      )}
      {menu === 'additionalFunctionality' && (
        <div className='flex-1'>
          <Header label='Additional Functionality' />
          <div className='px-8'>
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
            {/* Remove this feature for now as it slows down the frontend. */}
            {/* <Checkbox
              id='allPavedPaths'
              onChange={() => {
                setPavedPathsChecked(!pavedPathsChecked);
                toggleAllPathsDisplay('allPavedPaths', '/api/allpavedpaths');
              }}
              checked={pavedPathsChecked}
              label='Display All Paved Paths'
            /> */}
            {/* TOURLOOP FR22 : Toggle Location tracking */}
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
        </div>
      )}
    </div>
  );
};

export default Sidebar;
