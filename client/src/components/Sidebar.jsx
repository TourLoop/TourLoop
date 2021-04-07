import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { decode } from '@googlemaps/polyline-codec';

const Sidebar = props => {
  const { setPolylines } = props;
  const [loading, setLoading] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();

  const onSubmit = async data => {
    setLoading(true);
    const res = await fetch('/api', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });

    if (res.status === 200) {
      const route = await res.json();

      const latLngs = decode(route.path, 6);
      const polylines = latLngs.map(latLng => ({
        lat: latLng[0],
        lng: latLng[1],
      }));

      setPolylines([
        {
          paths: [polylines],
          display: true,
          id: 'temp',
          color: '#FF6347',
        },
      ]);
    } else {
      // error message
    }

    setLoading(false);
  };

  const downloadDatabaseFiles = () => {
    fetch('/export/tar')
      .then(response => response.blob())
      .then(blob => {
        // from https://medium.com/yellowcode/download-api-files-with-react-fetch-393e4dae0d9e
        // 2. Create blob link to download
        const url = window.URL.createObjectURL(new Blob([blob]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'tourloop-database-files.tar.gz');
        // 3. Append to html page
        document.body.appendChild(link);
        // 4. Force download
        link.click();
        // 5. Clean up and remove the link
        link.parentNode.removeChild(link);
      })
      .catch(error => {
        console.log(error);
      });
  };

  return (
    <div className='sidebar'>
      <h1 className='sidebar-header'>Generate Routes</h1>
      <form
        onSubmit={handleSubmit(onSubmit)}
        style={{ display: 'flex', flexDirection: 'column', padding: '2rem' }}
      >
        <label htmlFor='pointToPoint'>Point-to-Point</label>
        <input
          {...register('pointToPoint')}
          id='pointToPoint'
          type='checkbox'
          className='rounded text-blue-500 mb-4'
        />

        <label htmlFor='startLocation'>Start Location</label>
        <input
          {...register('startLocation', {
            required: true,
          })}
          id='startLocation'
          type='text'
          className='input'
        />

        <label htmlFor='endLocation'>End Location</label>
        <input
          {...register('endLocation')}
          id='endLocation'
          type='text'
          className='input'
        />

        <label htmlFor='targetRouteDistance'>Target Route Distance</label>
        <input
          {...register('targetRouteDistance', {
            required: true,
            valueAsNumber: true,
          })}
          id='targetRouteDistance'
          type='text'
          className='input'
        />

        <label htmlFor='pathType'>Path Type</label>
        <select {...register('pathType')} id='pathType' className='input'>
          <option value='bike'>Bike Path</option>
          <option value='paved'>Paved Road</option>
          <option value='dirt'>Dirt Trail</option>
        </select>

        <label htmlFor='algorithm'>Algorithm</label>
        <select {...register('algorithm')} id='algorithm' className='input'>
          <option value='pins'>Pins</option>
          <option value='algo1'>Algorithm 1</option>
          <option value='algo2'>Algorithm 2</option>
          <option value='algo3'>Algorithm 3</option>
        </select>

        <button type='submit' className='button'>
          Generate Routes
        </button>
      </form>
      <hr />
      <h1 className='sidebar-header'>Additional Functionality</h1>
      <div
        style={{ display: 'flex', flexDirection: 'column', padding: '2rem' }}
      >
        <label>Display All Dirt Paths</label>
        <input
          id='allDirtPaths'
          type='checkbox'
          className='rounded text-blue-500 mb-4'
          onClick={() => props.fetchAllPaths(false)}
        />
        <label>Display All Bike Paths</label>
        <input
          id='allBikePaths'
          type='checkbox'
          className='rounded text-blue-500 mb-4'
          onClick={() => props.fetchAllPaths(true)}
        />
        <label>Track Current Location</label>
        <input 
          id="locationToggle" 
          type="checkbox" 
          className='rounded text-blue-500 mb-4'
          onClick={() => props.setUseLocation(!props.useLocation) }
         />
        <button className='button' onClick={downloadDatabaseFiles}>
          Download Database
        </button>
      </div>
    </div>
  );
};

export default Sidebar;
