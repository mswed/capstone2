import { Container } from 'react-bootstrap';

const NotFound = () => {
  return (
    <Container>
      <h1 className="display-1">404</h1>
      <p className="lead">Not enough points! Solve Failed (i.e. check your URL you're trying to access a page that doesn't exist)</p>
    </Container>
  );
};

export default NotFound;
