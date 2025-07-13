import { Modal, Button } from 'react-bootstrap';

const ConfirmDialog = ({
  show,
  onConfirm,
  onCancel,
  title,
  message,
  confirmText = 'Confirm',
}) => {
  return (
    <Modal show={show} size="xl" centered>
      <Modal.Header closeButton>
        <Modal.Title>{title}</Modal.Title>
      </Modal.Header>
      <Modal.Body>{message}</Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={onCancel}>
          Cancel
        </Button>
        <Button variant="danger" onClick={onConfirm}>
          {confirmText}
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default ConfirmDialog;
