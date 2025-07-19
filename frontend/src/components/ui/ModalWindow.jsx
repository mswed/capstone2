import { Col, Container, Modal, Row } from 'react-bootstrap';

const ModalWindow = ({ show, onHide, title, form }) => {
  return (
    <Modal show={show} onHide={onHide} size="xl" centered>
      <Modal.Header closeButton>
        <Modal.Title>{title}</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Container fluid>{form}</Container>
      </Modal.Body>
    </Modal>
  );
};

export default ModalWindow;
