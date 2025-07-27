import { Form, Button } from 'react-bootstrap';
import { useState } from 'react';
import { Link } from 'react-router-dom';

const PasswordUpdateForm = ({ onSubmit, username }) => {
  const INITIAL_STATE = {
    password: '',
  };

  const showMessage = (message, status) => {
    console.log(message, status);
  };

  // Manage the form inputs
  const [paswordFormData, setPasswordFromData] = useState(INITIAL_STATE);

  const handleChange = (evt) => {
    const { name, value } = evt.target;
    setPasswordFromData((originalData) => ({ ...originalData, [name]: value }));
  };

  const handleSubmit = async (evt) => {
    evt.preventDefault();
    onSubmit(paswordFormData);
  };

  return (
    <>
      <Form onSubmit={handleSubmit}>
        <Form.Group className="mb-3" controlId="username">
          <Form.Label>Username</Form.Label>
          <Form.Control placeholder="Username" name="username" onChange={handleChange} value={username} disabled />
        </Form.Group>
        <Form.Group className="mb-3" controlId="password">
          <Form.Label>Password</Form.Label>
          <Form.Control type="password" placeholder="New Password" name="password" onChange={handleChange} value={paswordFormData.password} />
        </Form.Group>
        <Button type="submit" className="w-100">
          Update Password
        </Button>
      </Form>
    </>
  );
};

export default PasswordUpdateForm;
