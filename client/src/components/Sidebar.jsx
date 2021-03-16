const Sidebar = props => {
  const handleSubmit = () => {};

  return (
    <div className='sidebar'>
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
