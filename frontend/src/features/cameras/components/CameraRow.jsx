import { Link } from 'react-router-dom';

const CameraRow = ({ camera, showMake = true }) => {
  return (
    <tr>
      <td>
        <img src={camera.image ? camera.image : '/media/camera_images/missing_image.png'} alt={`Image of ${camera.model}`} style={{ width: '60px' }} />
      </td>
      {showMake && <td>{camera.make_name}</td>}
      <td>{camera.model}</td>
      <td>{camera.sensor_size}</td>
      <td>
        {camera.max_filmback_width}mm x {camera.max_filmback_height}mm
      </td>
      <td>
        {camera.max_image_width} x {camera.max_image_height}
      </td>
      <td>
        <Link to={`/cameras/${camera.id}`} className="btn btn-outline-primary btn-sm">
          View
        </Link>
      </td>
    </tr>
  );
};

export default CameraRow;
