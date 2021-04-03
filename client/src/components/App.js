import { useState, useEffect } from 'react';
import { decode } from '@googlemaps/polyline-codec';

import Map from './Map';
import Sidebar from './Sidebar';

const ALLPATHS = "ALLPATHS";
const ALLBIKEPATHS = "ALLBIKEPATHS";
const ALGO2 = "ALGO2";

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

  useEffect(() => {
    fetch("/api")
      .then(res => res.json())
      .then((line) => {
        let latLngs = [{ "paths": [[]], display: true, id: ALGO2, color: "#FF6347" }];
        var p = decode(line.path, 6)
        for (let j = 0; j < p.length; j++) {
          latLngs[0].paths[0].push({ lat: p[j][0], lng: p[j][1] });
        }
        setPolylines(latLngs)
        alert(`Time: ${line.time}, Distance: ${line.distance}, Percent Path Type: ${line.percentpathtype}`)
      },
        (error) => {
          console.log(error)
        }
      )
  }, []);

  return (
    <div className='app'>
      <Map polylines={polylines} />
      <Sidebar fetchAllPaths={fetchAllPaths} />
    </div>
  );
}

export default App;
