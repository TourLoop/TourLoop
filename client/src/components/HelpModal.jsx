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
          </div>
        </>,
        document.body
      )
    : null;
};

export default HelpModal;
