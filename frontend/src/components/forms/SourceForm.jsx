import { Form, Button } from 'react-bootstrap';
import { useState, useContext } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { AuthContext } from '../../context/AuthContext';

const SourceForm = ({ onSubmit, sourceData }) => {
  const INITIAL_STATE = {
    name: sourceData?.name ? sourceData.name : '',
    url: sourceData?.url ? sourceData.url : '',
    fileName: sourceData?.file_name ? sourceData.file_name : '',
    note: sourceData?.note ? sourceData.note : '',
  };

  // Manage the form inputs
  const [sourceFormData, setSourceFormData] = useState(INITIAL_STATE);

  const handleChange = (evt) => {
    const { name, value } = evt.target;
    setSourceFormData((originalData) => ({ ...originalData, [name]: value }));
  };

  const handleSubmit = async (evt) => {
    evt.preventDefault();
    onSubmit(sourceFormData);
  };

  return (
    <Form onSubmit={handleSubmit}>
      <Form.Group className="mb-3" controlId="name">
        <Form.Label>Name</Form.Label>
        <Form.Control placeholder="Alexa Mini Formats List" name="name" onChange={handleChange} value={sourceFormData.name} />
      </Form.Group>
      <Form.Group className="mb-3" controlId="url">
        <Form.Label>URL</Form.Label>
        <Form.Control placeholder="https://www.webpage.com" name="url" onChange={handleChange} value={sourceFormData.url} />
      </Form.Group>
      <Form.Group className="mb-3" controlId="file_name">
        <Form.Label>Filename</Form.Label>
        <Form.Control placeholder="alexa_formats_list.pdf" name="file_name" onChange={handleChange} value={sourceFormData.fileName} />
      </Form.Group>
      <Form.Group className="mb-3" controlId="note">
        <Form.Label>Note</Form.Label>
        <Form.Control placeholder="Some additional info" name="note" onChange={handleChange} value={sourceFormData.note} />
      </Form.Group>
      <Button type="submit" className="w-100">
        Add
      </Button>
    </Form>
  );
};

export default SourceForm;
