
import { useState, useEffect } from 'react';
import { GoogleMap, LoadScript } from '@react-google-maps/api';
import { Polyline } from '@react-google-maps/api';
import { decode } from '@googlemaps/polyline-codec';

const containerStyle = {
  width: '70vw',
  height: '100vh',
};

const center = {
  lat: 53.5461,
  lng: -113.4938,
};

const options = {
  strokeColor: '#FF0000',
  strokeOpacity: 0.8,
  strokeWeight: 2,
  fillColor: '#FF0000',
  fillOpacity: 0.35,
  clickable: false,
  draggable: false,
  editable: false,
  visible: true,
  zIndex: 1,
};

const Map = props => {
  const [polylines, setPolylines] = useState([]);

  useEffect(() => {
    fetch("/api")
      .then(res => res.json())
      .then((line) => {
        let latLngs = [];
        for (var i = 0; i < line.paths.length; i++) {
          latLngs.push([])
          var p = decode(line.paths[i], 6)
          for (let j = 0; j < p.length; j++) {
            latLngs[i].push({ lat: p[j][0], lng: p[j][1] });
          }
        }
        setPolylines(latLngs)
      },
        (error) => {
          console.log(error)
        }
      )
  }, []);

  return (
    <LoadScript googleMapsApiKey=''>
      <GoogleMap mapContainerStyle={containerStyle} center={center} zoom={11}>
        {polylines.map((polyline, i) => (
          <Polyline key={i} path={polyline} options={options} />
        ))}
        {/* Child components, such as markers, info windows, etc. */}
        <></>
      </GoogleMap>
    </LoadScript>
  );
};

export default Map;
