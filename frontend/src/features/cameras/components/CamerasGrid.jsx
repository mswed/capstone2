import { Link } from 'react-router-dom';
import { Row, Col } from 'react-bootstrap';
import CameraCard from './CameraCard';

const CameraGrid = ({ cameras }) => {
  return (
    <Row>
      {cameras.map((cam) => (
        <Col key={cam.id} xs={12} sm={6} md={4} className="px-3">
          <Link to={`/cameras/${cam.id}`} className="text-decoration-none">
            <CameraCard camera={cam} />
          </Link>
        </Col>
      ))}
    </Row>
  );
};

export default CameraGrid;
