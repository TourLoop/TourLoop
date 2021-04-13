import { useState, useEffect, useRef } from 'react';
import { decode } from '@googlemaps/polyline-codec';

import Map from './Map';
import Sidebar from './Sidebar';
import logo from '../assets/images/logo.png';

// const ALLDIRTPATHS = 'ALLDIRTPATHS';
// const ALLBIKEPATHS = 'ALLBIKEPATHS';
// const ALGO2 = 'ALGO2';

const DISCLAIMER_MESSAGE = `
DISCLAIMER:

TourLoop is not responsible for any inacuracies in map data. 
The data we have and the routes we generate may not be up to date, accurate, or safe.

Be aware of your surroundings. Use this application at your own risk. 
`;

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
  const [useLocation, setUseLocation] = useState(false);
  const [clickedLatLng, setClickedLatLng] = useState('');

  const startLocationInput = useRef(null);

  const onGoogleMapClick = e => {
    let lat = e.latLng.lat().toFixed(6);
    let lng = e.latLng.lng().toFixed(6);
    setClickedLatLng(`${lat}, ${lng}`);
    startLocationInput.current.value = `${lat}, ${lng}`;
  };

  // Current Location code to null island
  const defaultPosition = { lat: 0.0, lng: 0.0 }; // "null island"
  const [currPos, setCurrPos] = useState();
  // Update the location periodically
  const locationUpdateFrequency = 10; // seconds
  useEffect(() => {
    setTimeout(() => {
      // console.log("Trying to update current position...")
      // form https://developers.google.com/maps/documentation/javascript/geolocation
      if (useLocation) {
        if (navigator.geolocation) {
          navigator.geolocation.getCurrentPosition(
            position => {
              setCurrPos({
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
          console.log('geolocation not supported by browser');
        }
      } else {
        setCurrPos(defaultPosition);
      }
    }, 1000 * locationUpdateFrequency);
  });

  useEffect(() => {
    alert(DISCLAIMER_MESSAGE);
  }, []);

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

  // const fetchAllPaths = (bikesOnly = false) => {
  //   let id = ALLDIRTPATHS;
  //   let url = '/api/alldirtpaths';
  //   let pathColor = '#577590';
  //   if (bikesOnly) {
  //     id = ALLBIKEPATHS;
  //     url = '/api/allbikepaths';
  //     pathColor = '#4BA973';
  //   }

  //   let ind = polylines.findIndex(p => p.id === id);

  //   if (ind !== -1) {
  //     // We have already fetched all paths. Turn display on or off.
  //     let plines = [...polylines];
  //     let pline = { ...plines[ind] };
  //     pline.display = !pline.display;
  //     plines[ind] = pline;
  //     setPolylines(plines);
  //   } else {
  //     fetch(url)
  //       .then(res => res.text())
  //       .then(
  //         f => {
  //           let latLngs = {
  //             paths: [],
  //             display: true,
  //             id: id,
  //             color: pathColor,
  //           };
  //           f.split('\n').forEach(function (path) {
  //             var p = decode(path, 6);
  //             let pline = p.map(p => ({
  //               lat: p[0],
  //               lng: p[1],
  //             }));
  //             latLngs.paths.push(pline);
  //           });
  //           setPolylines([...polylines, latLngs]);
  //         },
  //         error => {
  //           console.log(error);
  //         }
  //       );
  //   }
  // };

  // useEffect(() => {
  //   fetch('/api')
  //     .then(res => res.json())
  //     .then(
  //       line => {
  //         let latLngs = [
  //           { path: [], display: true, id: ALGO2, color: '#FF6347' },
  //         ];
  //         var p = decode(line.path, 6);
  //         for (let j = 0; j < p.length; j++) {
  //           latLngs[0].path.push({ lat: p[j][0], lng: p[j][1] });
  //         }
  //         console.log(latLngs);
  //         setPolylines(latLngs);
  //       },
  //       error => {
  //         console.log(error);
  //       }
  //     );
  // }, []);

  return (
    <div className='app'>
      <img src={logo} className='logo' alt='Logo' />
      <Map
        polylines={polylines}
        position={currPos}
        onGoogleMapClick={onGoogleMapClick}
      />
      <Sidebar
        ref={startLocationInput}
        clickedLatLng={clickedLatLng}
        toggleDisplay={toggleDisplay}
        toggleAllPathsDisplay={toggleAllPathsDisplay}
        polylines={polylines}
        setPolylines={setPolylines}
        setUseLocation={setUseLocation}
        useLocation={useLocation}
      />
    </div>
  );
}

export default App;
