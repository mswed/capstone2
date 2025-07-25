import { Form, Button } from 'react-bootstrap';
import { useState } from 'react';
import { Link } from 'react-router-dom';

const LoginForm = ({ onSubmit, onSwitchToRegister }) => {
  const INITIAL_STATE = {
    username: '',
    password: '',
  };

  const showMessage = (message, status) => {
    console.log(message, status);
  };

  // Manage the form inputs
  const [loginForm, setLoginForm] = useState(INITIAL_STATE);

  const handleChange = (evt) => {
    const { name, value } = evt.target;
    setLoginForm((originalData) => ({ ...originalData, [name]: value }));
  };

  const handleSubmit = async (evt) => {
    evt.preventDefault();
    onSubmit(loginForm.username, loginForm.password);
  };

  return (
    <>
      <Form onSubmit={handleSubmit}>
        <Form.Group className="mb-3" controlId="username">
          <Form.Label>Username</Form.Label>
          <Form.Control placeholder="Username" name="username" onChange={handleChange} value={loginForm.username} />
        </Form.Group>
        <Form.Group className="mb-3" controlId="password">
          <Form.Label>Password</Form.Label>
          <Form.Control type="password" placeholder="Password" name="password" onChange={handleChange} value={loginForm.password} />
        </Form.Group>
        <Button type="submit" className="w-100">
          Login
        </Button>
      </Form>
      <div className="mt-3 text-muted">
        Don't have an account?{' '}
        <span>
          <Link onClick={() => onSwitchToRegister()}>Register</Link>
        </span>
      </div>
    </>
  );
};

export default LoginForm;
