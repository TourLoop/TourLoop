import { useState, useEffect } from 'react';
import { decode } from '@googlemaps/polyline-codec';

import Map from './Map';
import Sidebar from './Sidebar';
import logo from '../assets/images/logo.png';

const defaultPolylines = [
  {
    paths: [],
    display: true,
    id: 'allDirtPaths',
    color: '#577590',
  },
  {
    paths: [],
    display: true,
    id: 'allBikePaths',
    color: '#4BA973',
  },
  {
    paths: [],
    display: true,
    id: 'allPavedPaths',
    color: '#f09841',
  },
  {
    paths: [],
    display: true,
    id: 'algo1',
    color: '#FF6347',
  },
  {
    paths: [],
    display: true,
    id: 'algo2',
    color: '#3B82F6',
  },
  {
    paths: [],
    display: true,
    id: 'algo3',
    color: '#EC4899',
  },
];

function App() {
  // Current Location code to null island
  const defaultPosition = { lat: 0.0, lng: 0.0 }; // "null island"

  // polylines is of type
  // [{
  //    paths: [[{lat: float, lng: float}, ...]...],
  //    displayName: string,
  //    id: string,
  //    display: bool,
  //    color: string,
  //    time: string,
  // }, ...]
  const [polylines, setPolylines] = useState(defaultPolylines);
  const [startLocation, setStartLocation] = useState(defaultPosition);
  const [endLocation, setEndLocation] = useState(defaultPosition);
  const [currentLocation, setCurrentLocation] = useState(defaultPosition);
  const [useLocation, setUseLocation] = useState(false);
  const [pointToPointChecked, setPointToPointChecked] = useState(false);

  const onGoogleMapClick = e => {
    const coord = {
      lat: +e.latLng.lat().toFixed(6),
      lng: +e.latLng.lng().toFixed(6),
    };

    if (!startLocation.lat && !startLocation.lat) {
      setStartLocation(coord);
    } else if (pointToPointChecked && !endLocation.lat && !endLocation.lng) {
      setEndLocation(coord);
    } else if (!pointToPointChecked) {
      setStartLocation(coord);
    }
  };

  const onGoogleMapRightClick = e => {
    setStartLocation(defaultPosition);
    setEndLocation(defaultPosition);
  };

  // Update the location periodically
  const locationUpdateFrequency = 1; // seconds
  useEffect(() => {
    const updateLocation = setInterval(() => {
      // console.log("Trying to update current position...")
      // form https://developers.google.com/maps/documentation/javascript/geolocation
      if (useLocation) {
        if (navigator.geolocation) {
          navigator.geolocation.getCurrentPosition(
            position => {
              setCurrentLocation({
                lat: position.coords.latitude,
                lng: position.coords.longitude,
              });
            },
            error => {
              console.log('Something went wrong setting the current location');
              console.log(error);
            }
          );
        } else {
          // Browser doesn't support Geolocation
          console.log('Geolocation not supported by browser');
        }
      } else {
        setCurrentLocation(defaultPosition);
      }
    }, 1000 * locationUpdateFrequency);

    return () => clearInterval(updateLocation);
  }, [useLocation]);

  const toggleDisplay = id => {
    const newPolylines = polylines.map(p =>
      p.id === id ? { ...p, display: !p.display } : p
    );
    setPolylines(newPolylines);
  };

  const toggleAllPathsDisplay = (id, url) => {
    if (polylines.find(p => p.id === id).paths.length === 0) {
      fetchAllPaths({ id, url });
    } else {
      toggleDisplay(id);
    }
  };

  const fetchAllPaths = async reqOptions => {
    try {
      const res = await fetch(reqOptions.url);

      if (res.status === 200) {
        const routes = await res.text();

        const paths = routes.split('\n').map(route => {
          const latLngs = decode(route, 6);
          return latLngs.map(latLng => ({
            lat: latLng[0],
            lng: latLng[1],
          }));
        });

        const polyline = polylines.find(p => p.id === reqOptions.id);

        const newPolylines = polylines.map(p =>
          p.id === polyline.id
            ? {
                paths: paths,
                display: polyline.display,
                id: polyline.id,
                color: polyline.color,
              }
            : p
        );

        setPolylines(newPolylines);
      } else {
        // error message
      }
    } catch (e) {
      console.error('Error: ', e);
      // error message
    }
  };

  return (
    <div className='app'>
      <img src={logo} className='logo' alt='Logo' />
      <Map
        polylines={polylines}
        startLocation={startLocation}
        endLocation={endLocation}
        currentLocation={currentLocation}
        onGoogleMapClick={onGoogleMapClick}
        onGoogleMapRightClick={onGoogleMapRightClick}
      />
      <Sidebar
        startLocation={startLocation}
        setStartLocation={setStartLocation}
        endLocation={endLocation}
        setEndLocation={setEndLocation}
        toggleDisplay={toggleDisplay}
        toggleAllPathsDisplay={toggleAllPathsDisplay}
        polylines={polylines}
        setPolylines={setPolylines}
        setUseLocation={setUseLocation}
        useLocation={useLocation}
        pointToPointChecked={pointToPointChecked}
        setPointToPointChecked={setPointToPointChecked}
      />
    </div>
  );
}

export default App;
