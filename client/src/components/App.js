import { useState, useEffect } from 'react';
import { decode } from '@googlemaps/polyline-codec';

import Map from './Map';
import Sidebar from './Sidebar';

const ALLPATHS = "ALLPATHS";
const ALLBIKEPATHS = "ALLBIKEPATHS";

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

  const fetchAllPaths = (bikesOnly = false) => {
    let id = ALLPATHS
    let url = "/api/allpaths"
    let pathColor = "#577590"
    if (bikesOnly) {
      id = ALLBIKEPATHS
      url = "/api/allbikepaths"
      pathColor = "#4BA973"
    }


    let ind = polylines.findIndex(p => p.id === id)

    if (ind !== -1) {
      // We have already fetched all paths. Turn display on or off.
      polylines[ind].display = !polylines[ind].display
    } else {
      fetch(url)
        .then(res => res.text())
        .then((f) => {
          let latLngs = [{ "paths": [], display: true, id: id, color: pathColor }];
          f.split('\n').forEach(function (path) {
            var p = decode(path, 6)
            latLngs[0].paths.push([])
            for (let j = 0; j < p.length; j++) {
              latLngs[0].paths[latLngs[0].paths.length - 1].push({ lat: p[j][0], lng: p[j][1] });
            }
          })
          setPolylines(latLngs)
        },
          (error) => {
            console.log(error)
          }
        )
    }
  }

  return (
    <div className='app'>
      <Map polylines={polylines} />
      <Sidebar fetchAllPaths={fetchAllPaths} />
    </div>
  );
}

export default App;
