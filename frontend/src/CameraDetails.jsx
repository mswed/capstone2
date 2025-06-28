import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Container, Card, Row, Col } from 'react-bootstrap';
import GrumpyApi from './api';
import Loading from './Loading';
import FormatList from './FormatList.jsx';
import LocalSearchForm from './LocalSearchForm.jsx';

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

  if (isLoading) {
    return <Loading />;
  }

  return (
    <Container>
      <Card className="shadow-lg rounded-0 rounded-bottom">
        <Row className="g-0">
          <Col md={4}>
            <Card.Img
              src={cameraData.image ? cameraData.image : '/media/camera_images/missing_image.png'}
              alt={`Logo for ${cameraData.model}`}
              className="p-3"
              style={{
                objectFit: 'contain',
                maxHeight: '250px',
                maxWidth: '100%',
              }}
            />
          </Col>
          <Col md={5}>
            <Card.Body className="text-start">
              <Card.Title>{cameraData.model}</Card.Title>
              <dl className="row">
                <dt className="col-sm-4">Make:</dt>
                <dd className="col-sm-8">{cameraData.make_name}</dd>

                <dt className="col-sm-4">Sensor Type:</dt>
                <dd className="col-sm-8">{cameraData.sensor_type}</dd>

                <dt className="col-sm-4">Max Filmback:</dt>
                <dd className="col-sm-8">
                  {cameraData.max_filmback_width}mm x {cameraData.max_filmback_height}mm
                </dd>

                <dt className="col-sm-4">Max Resolution:</dt>
                <dd className="col-sm-8">
                  {cameraData.max_image_width} x {cameraData.max_image_height}
                </dd>

                <dt className="col-sm-4">Frame Rate:</dt>
                <dd className="col-sm-8">
                  {cameraData.min_frame_rate}fps - {cameraData.max_frame_rate}
                  fps
                </dd>
              </dl>
            </Card.Body>
          </Col>
          <Col md={3} className="text-start p-3">
            {cameraData.notes && (
              <div>
                <h6>Notes</h6>
                <p>{cameraData.notes}</p>
              </div>
            )}
          </Col>
        </Row>
      </Card>
      <Row className="mt-3">
        <Col>
          <Row>
            <LocalSearchForm
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
