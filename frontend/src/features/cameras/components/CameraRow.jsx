import { Link } from 'react-router-dom';
const baseUrl = import.meta.env.VITE_BASE_URL || 'http://127.0.0.1:8000/';

const CameraRow = ({ camera, showMake = true }) => {
  console.log('base url is', baseUrl);
  console.log('image is', camera.image);
  return (
    <tr>
      <td>
        <img src={camera.image ? camera.image : `${baseUrl}/media/camera_images/missing_image.png`} alt={`Image of ${camera.model}`} style={{ width: '60px' }} />
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
