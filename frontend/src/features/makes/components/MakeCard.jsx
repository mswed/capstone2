import { Card } from 'react-bootstrap';
const MakeCard = ({ name, logo, camCount }) => {
  return (
    <Card className="mt-3 h-100 shadow-lg">
      <Card.Img variant="top" src={logo} alt={`Logo for ${name}`} className="w-50 mx-auto mt-3" style={{ height: '150px', objectFit: 'contain' }} />
      <Card.Body>
        <Card.Title className="h5">{name}</Card.Title>
      </Card.Body>
      <Card.Footer className="text-muted">{camCount} Cameras</Card.Footer>
    </Card>
  );
};

export default MakeCard;
