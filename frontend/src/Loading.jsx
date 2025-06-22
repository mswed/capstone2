import { Container } from 'react-bootstrap';
const Loading = () => {
  return (
    <Container className="d-flex flex-column justify-content-center align-items-center min-vh-100 text-center" style={{ marginTop: '-5rem' }}>
      <h2 className="text-shadow">Loading...</h2>;
    </Container>
  );
};

export default Loading;
