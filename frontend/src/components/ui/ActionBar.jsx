import { useContext } from 'react';
import { Card, Button, Row, Col } from 'react-bootstrap';
import { AuthContext } from '../../context/AuthContext';

const ActionBar = ({ buttons = [], className = '' }) => {
  const { isAdmin } = useContext(AuthContext);
  const availableButtons = buttons.filter((button) => !button.adminOnly || isAdmin);

  if (availableButtons.length === 0) {
    return;
  }

  return (
    <Card className={`border-0 shadow-sm ${className}`}>
      <Card.Body className="py-2">
        <Row className="align-items-center">
          <Col className="text-end">
            {availableButtons.map((button, index) => (
              <Button
                key={index}
                variant={button.variant || 'primary'}
                size={button.size || 'sm'}
                className={`m-2 ${button.className || ''}`}
                onClick={button.onClick}
                disabled={button.disabled}
              >
                {button.text}
              </Button>
            ))}
          </Col>
        </Row>
      </Card.Body>
    </Card>
  );
};

export default ActionBar;
