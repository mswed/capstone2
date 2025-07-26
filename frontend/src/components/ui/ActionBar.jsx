import { Card, Button, Row, Col } from 'react-bootstrap';

const ActionBar = ({ buttons = [], className = '', isAdmin = false }) => {
  return (
    <Card className={`border-0 shadow-sm ${className}`}>
      <Card.Body className="py-2">
        <Row className="align-items-center">
          <Col className="text-end">
            {buttons
              .filter((button) => !button.adminOnly || isAdmin)
              .map((button, index) => (
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
