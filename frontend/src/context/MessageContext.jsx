import React, { useState } from 'react';

// We create the context
const MessageContext = React.createContext();

// We set up a component to manage the context
const MessagesProvider = ({ children }) => {
  const [message, setMessage] = useState(null);

  const showMessage = (text, variant = 'success', duration = 5000) => {
    setMessage({ text, variant, duration });
    // Auto clear
    if (duration) {
      setTimeout(() => {
        clearMessage();
      }, duration);
    }
  };

  const clearMessage = () => {
    setMessage(null);
  };

  return <MessageContext.Provider value={{ message, showMessage, clearMessage }}>{children}</MessageContext.Provider>;
};

export { MessageContext, MessagesProvider };
