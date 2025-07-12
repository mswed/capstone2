import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Container, Card, Row, Col } from 'react-bootstrap';
import GrumpyApi from '../../services/api';
import Loading from '../../components/ui/Loading';
import Checkmark from '../../components/ui/Checkmark';

const FormatDetails = () => {
  // Set up state
  const { formatId } = useParams();
  const [formatData, setFormatData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  const handleCopy = async (value) => {
    try {
      await navigator.clipboard.writeText(value);
    } catch (error) {
      consoel.error('Failed to copy:', error);
    }
  };
  // Fetch format data
  useEffect(() => {
    const getFormatDetails = async () => {
      try {
        const response = await GrumpyApi.getFormatDetails(formatId);
        setFormatData(response);
      } catch (error) {
        console.error('Error fetching camera details', error);
      } finally {
        setIsLoading(false);
      }
    };
    getFormatDetails();
  }, [formatId]);

  if (isLoading) {
    return <Loading />;
  }

  return (
    <Container>
      <Card className="shadow-lg rounded-0 rounded-bottom">
        <Row className="g-0">
          <Col md={3}>
            <Card.Img
              src="/film.png"
              alt="Film strip image"
              className="p-3"
              style={{
                objectFit: 'contain',
                maxHeight: '250px',
                maxWidth: '100%',
              }}
            />
          </Col>
          <Col md={4}>
            <Card.Body className="text-start">
              <Card.Title>
                {formatData.image_format} {formatData.image_aspect} {formatData.format_name}
              </Card.Title>
              <div>
                <dl className="row">
                  <dt className="col-sm-4">Make:</dt>
                  <dd className="col-sm-8">{formatData.make_name}</dd>

                  <dt className="col-sm-4">Model:</dt>
                  <dd className="col-sm-8">{formatData.camera_model}</dd>

                  <dt className="col-sm-4">Resolution:</dt>
                  <dd className="col-sm-8">
                    {formatData.image_width} x {formatData.image_height}
                  </dd>
                  <dt className="col-sm-4">Filmback:</dt>
                  <dd className="col-sm-8">
                    {formatData.sensor_width}mm x {formatData.sensor_height}mm
                  </dd>
                </dl>
              </div>
            </Card.Body>
          </Col>
          <Col md={5} className="text-start p-3">
            <div>
              <dl className="row">
                <dt className="col-sm-4">Anamorphic?:</dt>
                <dd className="col-sm-8">
                  <Checkmark checked={formatData.is_anamorphic} title="anamorphic?" />
                </dd>
                <dt className="col-sm-4">Desqueezed?:</dt>
                <dd className="col-sm-8">
                  <Checkmark checked={formatData.is_dequeezed} title="desqueezed?" />
                </dd>
                <dt className="col-sm-4">Pixel Aspect:</dt>
                <dd className="col-sm-8">{formatData.pixel_aspect}</dd>
                <dt className="col-sm-4">Downsampled?:</dt>
                <dd className="col-sm-8">
                  <Checkmark checked={formatData.is_downsampled} title="downsampled?" />
                </dd>
                <dt className="col-sm-4">Upscaled?:</dt>
                <dd className="col-sm-8">
                  <Checkmark checked={formatData.is_upscaled} title="upscaled?" />
                </dd>
                <dt className="col-sm-4">Codec:</dt>
                <dd className="col-sm-8">{formatData.codec}</dd>
                <dt className="col-sm-4">Raw recording available?:</dt>
                <dd className="col-sm-8">
                  <Checkmark checked={formatData.raw_recording_available} title="row recording available?" />
                </dd>
              </dl>
            </div>
          </Col>
        </Row>
      </Card>
      <Row className="mt-3">
        <Col>
          <Card className="shadow-lg">
            <Card.Body className="text-start">
              <Card.Title>Notes</Card.Title>
              <div>
                <dl>
                  {formatData.notes && <dt className="col-sm-4">Notes:</dt>}
                  {formatData.notes && <dd className="col-sm-8">{formatData.notes}</dd>}
                  {formatData.make_notes && <dt className="col-sm-4">Manufacturer Notes:</dt>}
                  {formatData.make_notes && <dd className="col-sm-8">{formatData.make_notes}</dd>}
                </dl>
              </div>
            </Card.Body>
          </Card>
        </Col>
      </Row>
      <Row className="mt-3">
        <Col md={6}>
          <Card className="shadow-lg">
            <Card.Body className="text-start">
              <Card.Title>3DE Info</Card.Title>
              <div>
                <dl className="row">
                  <dt className="col-sm-4">Filmback Width:</dt>
                  <dd className="col-md-8">
                    {formatData.filmback_width_3de}mm{' '}
                    <i
                      className="bi bi-copy text-muted ms-3"
                      role="button"
                      style={{ cursor: 'pointer' }}
                      aria-label="Copy"
                      onClick={() => handleCopy(formatData.filmback_width_3de)}
                    ></i>
                  </dd>
                  <dt className="col-sm-4">Filmback Height:</dt>
                  <dd className="col-md-8">
                    {formatData.filmback_height_3de}mm{' '}
                    <i
                      className="bi bi-copy text-muted ms-3"
                      role="button"
                      style={{ cursor: 'pointer' }}
                      aria-label="Copy"
                      onClick={() => handleCopy(formatData.filmback_height_3de)}
                    ></i>
                  </dd>
                  <dt className="col-sm-4">Distortion Model:</dt>
                  <dd className="col-sm-8">{formatData.distortion_model_3de}</dd>
                </dl>
              </div>
            </Card.Body>
          </Card>
        </Col>
        <Col md={6}>
          {formatData.tracking_workflow && (
            <Card className="shadow-lg">
              <Card.Body className="text-start">
                <div>
                  <dl className="row">
                    <dt className="col-sm-4">Tracking Workflow:</dt>
                    <dd className="col-sm-8">{formatData.tracking_workflow}</dd>
                  </dl>
                </div>
              </Card.Body>
            </Card>
          )}
        </Col>
      </Row>
    </Container>
  );
};

export default FormatDetails;
