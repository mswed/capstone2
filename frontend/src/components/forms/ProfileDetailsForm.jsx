import { Form, Button } from 'react-bootstrap';
import { useState } from 'react';

const ProfileDetailsForm = ({ onSubmit, userData }) => {
  const INITIAL_STATE = {
    username: userData?.username,
    email: userData?.email,
    firstName: userData?.firstName,
    lastName: userData?.lastName,
    role: userData?.role,
    studio: userData?.studio,
  };

  const showMessage = (message, status) => {
    console.log(message, status);
  };

  // Manage the form inputs
  const [profileDetailsFormData, setProfileDetailsFormData] = useState(INITIAL_STATE);

  const handleChange = (evt) => {
    const { name, value } = evt.target;
    setProfileDetailsFormData((originalData) => ({
      ...originalData,
      [name]: value,
    }));
  };

  const handleSubmit = async (evt) => {
    evt.preventDefault();
    onSubmit(profileDetailsFormData);
  };

  return (
    <>
      <Form onSubmit={handleSubmit}>
        <Form.Group className="mb-3" controlId="firstName">
          <Form.Label>First Name</Form.Label>
          <Form.Control placeholder="John" name="firstName" onChange={handleChange} value={profileDetailsFormData.firstName} />
        </Form.Group>
        <Form.Group className="mb-3" controlId="lastName">
          <Form.Label>Last Name</Form.Label>
          <Form.Control placeholder="Doe" name="lastName" onChange={handleChange} value={profileDetailsFormData.lastName} />
        </Form.Group>
        <Form.Group className="mb-3" controlId="email">
          <Form.Label>Email</Form.Label>
          <Form.Control type="email" placeholder="jdoe@studio.com" name="email" onChange={handleChange} value={profileDetailsFormData.email} />
        </Form.Group>
        <Form.Group className="mb-3" controlId="role">
          <Form.Label>Role</Form.Label>
          <Form.Control placeholder="Matchmove Artist" name="role" onChange={handleChange} value={profileDetailsFormData.role} />
        </Form.Group>
        <Form.Group className="mb-3" controlId="studio">
          <Form.Label>Studio</Form.Label>
          <Form.Control placeholder="The Best Studio" name="studio" onChange={handleChange} value={profileDetailsFormData.studio} />
        </Form.Group>
        <Button type="submit" className="w-100">
          Update
        </Button>
      </Form>
    </>
  );
};

export default ProfileDetailsForm;
