import { Form, Button } from 'react-bootstrap';
import { useState, useContext } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { AuthContext } from '../../context/AuthContext';

const MakeForm = ({ onSubmit, makeData }) => {
  const INITIAL_STATE = {
    name: makeData?.name ? makeData.name : '',
    website: makeData?.website ? makeData.website : '',
  };

  // Manage the form inputs
  const [makeFormData, setMakeformData] = useState(INITIAL_STATE);

  const handleChange = (evt) => {
    const { name, value, files } = evt.target;
    if (name === 'logo') {
      setMakeformData((originalData) => ({ ...originalData, logo: files[0] }));
    } else {
      setMakeformData((originalData) => ({ ...originalData, [name]: value }));
    }
  };

  const handleSubmit = async (evt) => {
    evt.preventDefault();
    onSubmit(makeFormData);
  };

  return (
    <Form onSubmit={handleSubmit}>
      <Form.Group className="mb-3" controlId="name">
        <Form.Label>Name</Form.Label>
        <Form.Control placeholder="Make Name" name="name" onChange={handleChange} value={makeFormData.name} />
      </Form.Group>
      <Form.Group className="mb-3" controlId="website">
        <Form.Label>Website</Form.Label>
        <Form.Control placeholder="https://www.webpage.com" name="website" onChange={handleChange} value={makeFormData.website} />
      </Form.Group>
      <Form.Group className="mb-3" controlId="logo">
        <Form.Label>Logo</Form.Label>
        <Form.Control type="file" name="logo" onChange={handleChange} />
      </Form.Group>
      <Button type="submit" className="w-100">
        Add
      </Button>
    </Form>
  );
};

export default MakeForm;
