import { Link } from 'react-router-dom';

const SourceRow = ({ source }) => {
  const cellStyle = {
    wordWrap: 'break-word',
    wordBreak: 'break-all',
    maxWidth: '0', // Forcing the text to wrap
  };

  return (
    <tr>
      <td className="text-start" style={cellStyle}>
        {source.name}
      </td>
      <td className="text-start" style={cellStyle}>
        {source.url}
      </td>
      <td className="text-start" style={cellStyle}>
        {source.fileName}
      </td>
      <td className="text-start" style={cellStyle}>
        {source.note}
      </td>
      <td>
        <Link
          to={`/sources/${source.id}`}
          className="btn btn-outline-primary btn-sm"
        >
          View
        </Link>
      </td>
    </tr>
  );
};

export default SourceRow;
