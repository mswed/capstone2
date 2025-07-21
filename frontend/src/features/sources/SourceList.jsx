import SourceRow from './SourceRow';
import { Table } from 'react-bootstrap';

const SourceList = ({ sources = [] }) => {
  return (
    <Table striped hover responsive size="sm" className="small" style={{ tableLayout: 'fixed' }}>
      <thead>
        <tr>
          <th style={{ width: '20%' }}>Name</th>
          <th style={{ width: '35%' }}>URL</th>
          <th style={{ width: '25%' }}>File Name</th>
          <th style={{ width: '15%' }}>Note</th>
          <th style={{ width: '5%' }}>Action</th>
        </tr>
      </thead>
      <tbody>
        {sources.map((source) => {
          return <SourceRow source={source} key={source.id} />;
        })}
      </tbody>
    </Table>
  );
};

export default SourceList;
