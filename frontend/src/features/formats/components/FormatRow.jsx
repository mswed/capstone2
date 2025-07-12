import { Button } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import Checkmark from '../../../components/ui/Checkmark';
import VoteWidget from './VoteWidget';

const FormatRow = ({ format, showModel = true, showAddButton = false, onFormatAdd }) => {
  const handleAdd = () => {
    if (onFormatAdd) {
      onFormatAdd(format.id);
    }
  };
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
        <Checkmark checked={format.is_anamorphic} title="anamorphic?" />
      </td>
      <td className="text-center">
        <Checkmark checked={format.is_desqueezed} title="desqueezed?" />
      </td>
      <td>
        <VoteWidget />
      </td>
      <td>
        {showAddButton ? (
          <Button variant="outline-danger" size="sm" onClick={handleAdd}>
            Add
          </Button>
        ) : (
          <Link to={`/formats/${format.id}`} className="btn btn-outline-primary btn-sm">
            View
          </Link>
        )}
      </td>
    </tr>
  );
};

export default FormatRow;
