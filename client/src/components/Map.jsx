import {
  GoogleMap,
  Marker,
  LoadScript,
  Polyline,
} from '@react-google-maps/api';

const center = {
  lat: 53.5461,
  lng: -113.4938,
};

const Map = props => {
  const { clickedLatLng, position } = props;

  return (
    <LoadScript googleMapsApiKey=''>
      <GoogleMap
        mapContainerClassName='map'
        center={center}
        zoom={11}
        onClick={props.onGoogleMapClick}
      >
        <Marker position={position} />;
        <Marker position={clickedLatLng} />;
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
            return <Polyline key={j} path={path} options={opt} />;
          });
        })}
        {/* Child components, such as markers, info windows, etc. */}
        <></>
      </GoogleMap>
    </LoadScript>
  );
};

export default Map;
