import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Container, Card, Row, Col } from 'react-bootstrap';
import GrumpyApi from './api';
import Loading from './Loading';
import FormatList from './FormatList.jsx';
import SimpleSearchFrom from './SimpleSearchForm.jsx';

const CameraDetails = () => {
  // Set up state
  const { cameraId } = useParams();
  const [cameraData, setCameraData] = useState(null);
  const [formatsData, setFormatsData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  // Fetch camera data
  useEffect(() => {
    const getCameraDetails = async () => {
      try {
        const response = await GrumpyApi.getCameraDetails(cameraId);
        setCameraData(response);
        setFormatsData(response.formats);
      } catch (error) {
        console.error('Error fetching camera details', error);
      } finally {
        setIsLoading(false);
      }
    };
    getCameraDetails();
  }, [cameraId]);

  console.log('formatsData length', formatsData?.length);
  if (isLoading) {
    return <Loading />;
  }

  return (
    <Container>
      <Row className="g-4 shadow-lg">
        <Col md={4}>
          <Card.Img
            src={cameraData.image ? cameraData.image : '/media/camera_images/missing_image.png'}
            alt={`Logo for ${cameraData.model}`}
            className="h-100 py-3"
            style={{ objectFit: 'cover' }}
          />
        </Col>
        <Col md={4}>
          <Card.Title>{cameraData.model}</Card.Title>
          <Card.Body className="mt-3">
            <ul>
              <li>Make: {cameraData.make_name}</li>
              <li>Sensor Type: {cameraData.sensor_type}</li>
              <li>
                Max Filmback: {cameraData.max_filmback_width}mm x {cameraData.max_filmback_height}mm
              </li>
              <li>
                Max Resolution: {cameraData.max_image_width} x {cameraData.max_image_height}
              </li>
              <li>
                Frame Rate: {cameraData.min_frame_rate}fps - {cameraData.max_frame_rate}fps
              </li>
            </ul>
          </Card.Body>
        </Col>
        <Col md={4}>
          {cameraData.notes && (
            <div>
              <h6>Notes</h6>
              <p>{cameraData.notes}</p>
            </div>
          )}
        </Col>
      </Row>
      <Row className="mt-3">
        <Col>
          <Row>
            <SimpleSearchFrom
              fields={['image_format', 'image_aspect', 'format_name']}
              targetArray={formatsData}
              setTargetArray={setFormatsData}
              originalArray={cameraData.formats}
            />
          </Row>
          <Row>
            <FormatList formats={formatsData} />
          </Row>
        </Col>
      </Row>
    </Container>
  );
};

export default CameraDetails;
