import { Form, Button } from 'react-bootstrap';
import { useState } from 'react';
import { Link } from 'react-router-dom';

const SignupForm = ({ onSubmit, onSwitchToLogin }) => {
  const INITIAL_STATE = {
    firstName: '',
    lastName: '',
    email: '',
    studio: '',
    role: '',
    username: '',
    password: '',
  };

  const showMessage = (message, status) => {
    console.log(message, status);
  };

  // Manage the form inputs
  const [signupFormData, setSignupFormData] = useState(INITIAL_STATE);

  const handleChange = (evt) => {
    const { name, value } = evt.target;
    setSignupFormData((originalData) => ({ ...originalData, [name]: value }));
  };

  const handleSubmit = async (evt) => {
    evt.preventDefault();
    onSubmit(signupFormData);
  };

  return (
    <>
      <Form onSubmit={handleSubmit}>
        <Form.Group className="mb-3" controlId="firstName">
          <Form.Label>First Name</Form.Label>
          <Form.Control placeholder="John" name="firstName" onChange={handleChange} value={signupFormData.firstName} />
        </Form.Group>
        <Form.Group className="mb-3" controlId="lastName">
          <Form.Label>Last Name</Form.Label>
          <Form.Control placeholder="Doe" name="lastName" onChange={handleChange} value={signupFormData.lastName} />
        </Form.Group>
        <Form.Group className="mb-3" controlId="email">
          <Form.Label>Email</Form.Label>
          <Form.Control type="email" placeholder="jdoe@studio.com" name="email" onChange={handleChange} value={signupFormData.email} />
        </Form.Group>
        <Form.Group className="mb-3" controlId="role">
          <Form.Label>Role</Form.Label>
          <Form.Control placeholder="Matchmove Artist" name="role" onChange={handleChange} value={signupFormData.role} />
        </Form.Group>
        <Form.Group className="mb-3" controlId="studio">
          <Form.Label>Studio</Form.Label>
          <Form.Control placeholder="The Best Studio" name="studio" onChange={handleChange} value={signupFormData.studio} />
        </Form.Group>
        <Form.Group className="mb-3" controlId="username">
          <Form.Label className="required-field">Username</Form.Label>
          <Form.Control placeholder="Username" name="username" onChange={handleChange} value={signupFormData.username} required />
        </Form.Group>
        <Form.Group className="mb-3" controlId="password">
          <Form.Label className="required-field">Password</Form.Label>
          <Form.Control type="password" placeholder="Password" name="password" onChange={handleChange} value={signupFormData.password} required />
        </Form.Group>
        <Button type="submit" className="w-100">
          Signup
        </Button>
      </Form>
      <div className="mt-3 text-muted">
        Already have an account?{' '}
        <span>
          <Link onClick={() => onSwitchToLogin()}>Login</Link>
        </span>
      </div>
    </>
  );
};

export default SignupForm;
