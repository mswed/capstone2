import { useContext } from 'react';
import { ToastContainer, Toast } from 'react-bootstrap';
import { MessageContext } from '../../context/MessageContext';

const Messages = () => {
  const { message, clearMessage } = useContext(MessageContext);

  if (!message) return null;

  // Function to render the message text properly based on type
  const renderMessageContent = () => {
    // If text is an array, render each item as a separate line
    if (Array.isArray(message.text)) {
      return (
        <>
          {message.text.map((line, index) => (
            <div key={index}>{line}</div>
          ))}
        </>
      );
    }
    // Otherwise just render the text directly
    return message.text;
  };

  return (
    <ToastContainer position="top-center" className="p-3">
      <Toast onClose={clearMessage} show={message} delay={message.duration} autohide={!!message.duration} bg={message.variant}>
        <Toast.Header>
          <strong className="me-auto">
            {message.variant === 'warning' ? 'Warning' : message.variant === 'danger' ? 'Error' : message.variant === 'success' ? 'Success' : 'Information'}
          </strong>
        </Toast.Header>
        <Toast.Body>{renderMessageContent()}</Toast.Body>
      </Toast>
    </ToastContainer>
  );
};

export default Messages;
