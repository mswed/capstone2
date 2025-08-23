import { Link } from 'react-router-dom';

const CameraRow = ({ camera, showMake = true }) => {
  return (
    <tr>
      <td>
        <img src={camera.image ? camera.image : '/media/camera_images/missing_image.png'} alt={`Image of ${camera.model}`} style={{ width: '60px' }} />
      </td>
      {showMake && <td>{camera.makeName}</td>}
      <td>{camera.model}</td>
      <td>{camera.sensorType}</td>
      <td>
        {camera.maxFilmbackWidth}mm x {camera.maxFilmbackHeight}mm
      </td>
      <td>
        {camera.maxImageWidth} x {camera.maxImageHeight}
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
