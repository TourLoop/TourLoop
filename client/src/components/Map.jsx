import { GoogleMap, LoadScript } from '@react-google-maps/api';

const containerStyle = {
  width: '100vw',
  height: '100vh',
};

const center = {
  lat: 53.5461,
  lng: -113.4938,
};

const Map = props => {
  return (
    <LoadScript googleMapsApiKey=''>
      <GoogleMap mapContainerStyle={containerStyle} center={center} zoom={11}>
        {/* Child components, such as markers, info windows, etc. */}
        <></>
      </GoogleMap>
    </LoadScript>
  );
};

export default Map;
