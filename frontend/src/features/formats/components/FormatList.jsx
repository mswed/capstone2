import FormatRow from './FormatRow.jsx';
import { Table } from 'react-bootstrap';

const FormatList = ({ formats, showModel = false, showAddButton = false, onFormatAdd }) => {
  return (
    <Table striped hover responsive size="sm" className="small">
      <thead>
        <tr>
          {showModel && <th>Make</th>}
          {showModel && <th>Model</th>}
          <th>Format</th>
          <th>Resolution</th>
          <th>Filmback</th>
          <th>PAR</th>
          <th>Anamorphic?</th>
          <th>Desqueezed?</th>
          <th></th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        {formats.map((format) => {
          return <FormatRow format={format} showModel={showModel} showAddButton={showAddButton} onFormatAdd={onFormatAdd} key={format.id} />;
        })}
      </tbody>
    </Table>
  );
};

export default FormatList;
