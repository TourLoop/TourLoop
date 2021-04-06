import { useState, useEffect } from 'react';
import { decode } from '@googlemaps/polyline-codec';

import Map from './Map';
import Sidebar from './Sidebar';

const ALLDIRTPATHS = 'ALLDIRTPATHS';
const ALLBIKEPATHS = 'ALLBIKEPATHS';
const ALGO2 = 'ALGO2';

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
  const [polylines, setPolylines] = useState([]);

  // Current Location code to null island 
  const [currPos, setCurrPos] = useState({lat:0.0, lng:0.0});
  // Update the location periodically 
  const locationUpdateFrequency = 10; // seconds 
  useEffect(() => {
    const timer = setTimeout(() => {
      console.log("Trying to update current position...")
      // form https://developers.google.com/maps/documentation/javascript/geolocation
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
          (position) => {
            setCurrPos({
              lat: position.coords.latitude,
              lng: position.coords.longitude,
            });
          },
          (error) => {
            console.log("Something went wrong setting the current location")
            console.log(error)
          }
        );
      } else {
        // Browser doesn't support Geolocation
        console.log("geolocation not supported by browser")
      }
    }, 1000*locationUpdateFrequency);
  });

  const fetchAllPaths = (bikesOnly = false) => {
    let id = ALLDIRTPATHS;
    let url = '/api/alldirtpaths';
    let pathColor = '#577590';
    if (bikesOnly) {
      id = ALLBIKEPATHS;
      url = '/api/allbikepaths';
      pathColor = '#4BA973';
    }

    let ind = polylines.findIndex(p => p.id === id);

    if (ind !== -1) {
      // We have already fetched all paths. Turn display on or off.
      let plines = [...polylines]
      let pline = { ...plines[ind] }
      pline.display = !pline.display
      plines[ind] = pline
      setPolylines(plines)
    } else {
      fetch(url)
        .then(res => res.text())
        .then(
          f => {
            let latLngs = { "paths": [], display: true, id: id, color: pathColor };
            f.split('\n').forEach(function (path) {
              var p = decode(path, 6);
              let pline = p.map(p => ({
                lat: p[0],
                lng: p[1],
              }));
              latLngs.paths.push(pline)
            });
            setPolylines([...polylines, latLngs]);
          },
          error => {
            console.log(error);
          }
        );
    }
  };

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
      <Map polylines={polylines} position={currPos}/>
      <Sidebar fetchAllPaths={fetchAllPaths} setPolylines={setPolylines} />
    </div>
  );
}

export default App;
