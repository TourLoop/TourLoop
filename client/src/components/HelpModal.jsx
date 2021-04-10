import ReactDOM from 'react-dom';

const HELPTEXT = `
TODO: add some helpful text

Coordinate input box format: lat-decimal, lon-decimal
Example: 
53.509905, -113.541233

The target distance is to be entered in kilometers
4.5 km should be entered as 4.5
500 meters should be entered as 0.5
`;

const HelpModal = props => {
  const { isShowing, hide } = props;

  return isShowing
    ? ReactDOM.createPortal(
        <>
          <div
            onClick={hide}
            className='fixed inset-0 bg-black opacity-25 z-50'
          />
          <div
            className='help-modal'
            style={{
              top: '50%',
              left: '50%',
              transform: 'translate(-50%, -50%)',
            }}
          >
            <h1 className='help-modal-header'>Help</h1>

            <h2 className='help-modal-header'>Generate Routes Info</h2>
            <p className='help-modal-text'>
              Coordinate input box format: lat-decimal, lon-decimal{' '}
            </p>
            <p className='help-modal-text'>Example:</p>
            <p className='help-modal-text'>53.509905, -113.541233</p>
            <p className='help-modal-text'>
              The target distance is to be entered in kilometers:
            </p>
            <p className='help-modal-text'>* 4.5 km should be entered as 4.5</p>
            <p className='help-modal-text'>
              * 500 meters should be entered as 0.5
            </p>

            <h2 className='help-modal-header'>Route Legend Info</h2>
            <p className='help-modal-text'>As you generate routes they will show up in the Routes Legend</p>
            <p className='help-modal-text'>Generated route overlays can be toggled in this menu</p>
            <p className='help-modal-text'>In this menu you will also see additional information on the generated routes</p>

            <h2 className='help-modal-header'>Additional Features Info</h2>
            <p className='help-modal-text'>In this menu you can toggle the different path type overlays onto the map</p>
            <p className='help-modal-text'>The available overlays are all paths, all bike path and all dirt paths</p>
            <p className='help-modal-text'>In this menu you can also toggle current location tracking</p>
            <p className='help-modal-text'>Your current location will update every 10 seconds</p>
            <p className='help-modal-text'>Location accuracy may varry</p>
            <p className='help-modal-text'>This menu is also where you can download the database</p>

          </div>
        </>,
        document.body
      )
    : null;
};

export default HelpModal;
