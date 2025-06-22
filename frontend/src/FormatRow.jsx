import { Link } from 'react-router-dom';

const FormatRow = ({ format, showModel = true }) => {
  return (
    <tr>
      {showModel && <td>{format.make_name}</td>}
      {showModel && <td>{format.camera_model}</td>}
      <td>
        {format.image_format} {format.image_aspect} {format.format_name}
      </td>
      <td>
        {format.image_width} x {format.image_height}
      </td>
      <td>
        {format.sensor_width}mm x {format.sensor_height}mm
      </td>
      <td>{format.pixel_aspect}</td>
      <td className="text-center">
        <span className={format.is_anamorphic ? 'text-success' : 'text-danger'}>{format.is_anamorphic ? '✓' : '✗'}</span>
      </td>
      <td className="text-center">
        <span className={format.is_desqueezed ? 'text-success' : 'text-danger'}>{format.is_desqueezed ? '✓' : '✗'}</span>
      </td>
      <td>
        <Link to={`/cameras/${format.id}`} className="btn btn-outline-primary btn-sm">
          View
        </Link>
      </td>
    </tr>
  );
};

export default FormatRow;
