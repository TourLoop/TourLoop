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

const polylines = [
  [
    { lat: 53.5414128, lng: -113.7135328 },
    { lat: 53.5414266, lng: -113.7201359 },
    { lat: 53.5414309, lng: -113.7270416 },
    { lat: 53.5414371, lng: -113.7370375 },
  ],
  [
    { lat: 53.552995, lng: -113.5085157 },
    { lat: 53.5514151, lng: -113.5084944 },
  ],
];

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
