import { Card } from 'react-bootstrap';
const CameraCard = ({ camera }) => {
  return (
    <Card className="h-50 shadow-lg">
      <Card.Img variant="top" src={camera.image} alt={`Image for ${camera.model}`} className="w-50 mx-auto mt-3" style={{ height: '200', objectFit: 'contain' }} />
      <Card.Body>
        <Card.Text className="fs-6 text-center mb-1">
          {camera.make_name} {camera.model}
        </Card.Text>
      </Card.Body>
    </Card>
  );
};

export default CameraCard;
