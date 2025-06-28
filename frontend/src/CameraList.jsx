import { useState } from 'react';
import CameraRow from './CameraRow';
import { Table } from 'react-bootstrap';

const CameraList = ({ cameras = [], showMake = false }) => {
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
          return <CameraRow camera={cam} showMake={showMake} key={cam.id} />;
        })}
      </tbody>
    </Table>
  );
};

export default CameraList;
