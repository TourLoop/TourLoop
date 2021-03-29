const Sidebar = props => {
  const handleSubmit = () => {};
  const downloadDatabaseFiles = () => {
    fetch("/export/tar")
    .then((response) => response.blob())
    .then((blob) => {
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
    }).catch((error) => {
      console.log(error)
    })
  }

  return (
    <div className='sidebar'>
      <button onClick={downloadDatabaseFiles}>Download Database Files</button>
      <h1 className='sidebar-header'>Generate Routes</h1>
      <form
        onSubmit={handleSubmit}
        style={{ display: 'flex', flexDirection: 'column', padding: '2rem' }}
      >
        <label htmlFor='pointToPoint'>Point-to-Point</label>
        <input
          id='pointToPoint'
          type='checkbox'
          className='rounded text-blue-500 mb-4'
        />
        <label htmlFor='startLoction'>Start Location</label>
        <input id='startLoction' type='text' className='input' />
        <label htmlFor='endLocation'>End Location</label>
        <input id='endLocation' type='text' className='input' />
        <label htmlFor='targetRouteDistance'>Target Route Distance</label>
        <input id='targetRouteDistance' type='text' className='input' />
        <label htmlFor='pathType'>Path Type</label>
        <select className='input'>
          <option>Bike Path</option>
          <option>Paved Road</option>
          <option>Dirt Trail</option>
        </select>
        <label htmlFor='algorithm'>Algorithm</label>
        <select className='input'>
          <option>Algorithm 1</option>
          <option>Algorithm 2</option>
          <option>Algorithm 3</option>
        </select>
        <button type='button' className='button'>
          Generate Routes
        </button>
      </form>
    </div>
  );
};

export default Sidebar;
