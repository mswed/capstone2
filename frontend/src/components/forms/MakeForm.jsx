import { Form, Button } from 'react-bootstrap';
import { useState } from 'react';

const MakeForm = ({ onSubmit, makeData, buttonLabel = 'Add' }) => {
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
        <Form.Label className="required-field">Name</Form.Label>
        <Form.Control placeholder="Make Name" name="name" onChange={handleChange} value={makeFormData.name} required />
      </Form.Group>
      <Form.Group className="mb-3" controlId="website">
        <Form.Label className="required-field">Website</Form.Label>
        <Form.Control placeholder="https://www.webpage.com" name="website" onChange={handleChange} value={makeFormData.website} required />
      </Form.Group>
      <Form.Group className="mb-3" controlId="logo">
        <Form.Label>Logo</Form.Label>
        <Form.Control type="file" name="logo" onChange={handleChange} />
      </Form.Group>
      <Button type="submit" className="w-100">
        {buttonLabel}
      </Button>
    </Form>
  );
};

export default MakeForm;
