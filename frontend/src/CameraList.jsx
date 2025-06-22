import { useState } from 'react';
import CameraRow from './CameraRow';
import { Table } from 'react-bootstrap';

const CameraList = ({ cams = null, showMake = false }) => {
  console.log('cameras are', cams);
  const [cameras, setCameras] = useState(cams);

  return (
    <Table striped hover responsive>
      <thead>
        <tr>
          <th>Image</th>
          {showMake && <th>Make</th>}
          <th>Model</th>
          <th>Sensor Size</th>
          <th>Max Filmback Size</th>
          <th>Max Resolution</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        {cameras.map((cam) => {
          console.log('strange', cam);
          return <CameraRow camera={cam} showMake={showMake} key={cam.id} />;
        })}
      </tbody>
    </Table>
  );
};

export default CameraList;
