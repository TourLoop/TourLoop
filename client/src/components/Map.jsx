import { GoogleMap, LoadScript, Polyline } from '@react-google-maps/api';

const containerStyle = {
  width: '70vw',
  height: '100vh',
};

const center = {
  lat: 53.5461,
  lng: -113.4938,
};

const Map = props => {
  return (
    <LoadScript googleMapsApiKey=''>
      <GoogleMap
        mapContainerStyle={containerStyle}
        center={center}
        zoom={11}
        on
      >
        {props.polylines.map((polyline, i) => {
          const opt = {
            strokeColor: polyline.color,
            strokeOpacity: 0.8,
            strokeWeight: 2,
            fillColor: polyline.color,
            fillOpacity: 0.35,
            clickable: false,
            draggable: false,
            editable: false,
            visible: polyline.display,
            zIndex: 1,
          };
          return polyline.paths.map((path, j) => {
            return < Polyline key={j} path={path} options={opt} />;
          });
        })}
        {/* Child components, such as markers, info windows, etc. */}
        <></>
      </GoogleMap>
    </LoadScript>
  );
};

export default Map;
