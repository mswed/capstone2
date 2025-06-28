import { useState } from 'react';
import FormatRow from './FormatRow.jsx';
import { Table } from 'react-bootstrap';

const FormatList = ({ formats = [], showModel = false }) => {
  return (
    <Table striped hover responsive>
      <thead>
        <tr>
          {showModel && <th>Make</th>}
          {showModel && <th>Model</th>}
          <th>Format</th>
          <th>Resolution</th>
          <th>Filmback</th>
          <th>Pixel Aspect</th>
          <th>Anamorphic?</th>
          <th>Desqueezed?</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        {formats.map((format) => {
          return <FormatRow format={format} showModel={showModel} key={format.id} />;
        })}
      </tbody>
    </Table>
  );
};

export default FormatList;
