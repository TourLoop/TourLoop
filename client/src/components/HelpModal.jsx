import ReactDOM from 'react-dom';
import { ReactComponent as Cancel } from '../assets/images/cancel.svg';

// TOURLOOP FR24 : Open Basic Instructions
// TOURLOOP FR25 : Close basic instructions
const HelpModal = props => {
  const { isShowing, hide } = props;

  return isShowing
    ? ReactDOM.createPortal(
        <>
          <div onClick={hide} className='help-modal-overlay' />
          <div
            className='help-modal'
            style={{
              top: '50%',
              left: '50%',
              transform: 'translate(-50%, -50%)',
            }}
          >
            <div className='flex justify-between items-center'>
              <h1 className='help-modal-header'>Help</h1>
              <Cancel className='help-modal-icon' onClick={hide} />
            </div>
            <div className='help-modal-section'>
              <h2 className='help-modal-section-header'>User Guide</h2>
              <p className='help-modal-text'>
                To generate a route, you can start by clicking on the map to set
                the latitude and longitude coordinate. In the generate routes
                form, type in a target route distance, select a path preference,
                select an algorithm, then click "Generate Route." Click on a
                different point on the map to change the latitude and longitude
                coordinate. Right-click to clear point.
              </p>
              <p className='help-modal-text'>
                If point-to-point is selected, you can click up to two points.
                One for start location and one for end location. Right-click to
                clear points and create two new points.
              </p>
            </div>
            <div className='help-modal-section'>
              <h2 className='help-modal-section-header'>
                Generate Routes Info
              </h2>
              <p className='help-modal-text'>
                Coordinate input box format: "latitude, longitude"
              </p>
              <p className='help-modal-text'>Example: 53.509905, -113.541233</p>
              <p className='help-modal-text'></p>
              <p className='help-modal-text'>
                The target distance is to be entered in kilometers:
              </p>
              <p className='help-modal-text'>
                * 4.5 km should be entered as 4.5
              </p>
              <p className='help-modal-text'>
                * 500 meters should be entered as 0.5
              </p>
            </div>
            <div className='help-modal-section'>
              <h2 className='help-modal-section-header'>Route Legend Info</h2>
              <p className='help-modal-text'>
                As you generate routes, they will show up in this menu.
                Generated route overlays can be toggled.
              </p>
              <p className='help-modal-text'>
                In this menu, you will also see additional information on the
                generated routes.
              </p>
            </div>
            <div className='help-modal-section'>
              <h2 className='help-modal-section-header'>
                Additional Features Info
              </h2>
              <p className='help-modal-text'>
                In this menu, you can toggle the different path type overlays
                onto the map. The available overlays are all paved paths, all
                bike paths, and all dirt paths.
              </p>
              <p className='help-modal-text'>
                In this menu, you can also toggle current location tracking.
                Your current location will update every second.
              </p>
              <p className='help-modal-text'>
                This is also where you can download the data source for this
                database.
              </p>
            </div>
            <div className='help-modal-section'>
              <h2 className='help-modal-section-header'>Disclaimer</h2>
              <p className='help-modal-text'>
                TourLoop is not responsible for any inaccuracies in map data.
                The data we have and the routes we generate may not be up to
                date, accurate, or safe.
              </p>
              <p className='help-modal-text'>
                Be aware of your surroundings. Use this application at your own
                risk.
              </p>
            </div>
          </div>
        </>,
        document.body
      )
    : null;
};

export default HelpModal;
