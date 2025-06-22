import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Container, Card, Row, Col } from 'react-bootstrap';
import GrumpyApi from './api';
import Loading from './Loading';
import CameraList from './CameraList';

const MakeDetails = () => {
  const { makeId } = useParams();
  const [makeData, setMakeData] = useState(null);

  // We need to check if we're still loading so we won't run into trying to
  // render a null state
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const getMakeDetails = async () => {
      try {
        const response = await GrumpyApi.getMakeDetails(makeId);
        setMakeData(response);
      } catch (error) {
        console.error('Error fetching make details', error);
      } finally {
        console.log('Got makes', makeData);
        setIsLoading(false);
      }
    };
    getMakeDetails();
  }, [makeId]);

  if (isLoading) {
    return <Loading />;
  }
  return (
    <Container>
      <Row className="g-3 shadow-lg">
        <Col md={4}>
          <Card.Img src={makeData.logo} alt={`Logo for ${makeData.name}`} className="h-100 py-3" style={{ objectFit: 'cover' }} />
        </Col>
        <Col md={8}>
          <Card.Title>{makeData.name}</Card.Title>
          <Card.Text>{makeData.website}</Card.Text>
        </Col>
      </Row>
      <Row className="mt-3">
        <CameraList cams={makeData.cameras} />
      </Row>
    </Container>
  );
};

export default MakeDetails;
