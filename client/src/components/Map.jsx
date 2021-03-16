import { GoogleMap, LoadScript } from '@react-google-maps/api';
import { Polyline } from '@react-google-maps/api';

const containerStyle = {
  width: '70vw',
  height: '100vh',
};

const center = {
  lat: 53.5461,
  lng: -113.4938,
};

// const polylines = [
//   {
//     path: [
//       {
//         lat: 1,
//         lng: 1,
//       },
//     ],
//   },
// ];

const Map = props => {
  return (
    <LoadScript googleMapsApiKey=''>
      <GoogleMap mapContainerStyle={containerStyle} center={center} zoom={11}>
        {/* {polylines.map((polyline, i) => (
          <Polyline key={i} path={polyline.path} />
        ))} */}
        {/* Child components, such as markers, info windows, etc. */}
        <></>
      </GoogleMap>
    </LoadScript>
  );
};

export default Map;
