import { Form, Button } from 'react-bootstrap';
import { useState } from 'react';

const CameraForm = ({ onSubmit, camData, buttonLabel = 'Add' }) => {
  const INITIAL_STATE = {
    model: camData?.model ? camData.model : '',
    sensorType: camData?.sensorType ? camData.sensorType : '',
    sensorSize: camData?.sensorSize ? camData.sensorSize : '',
    maxFilmbackWidth: camData?.maxFilmbackWidth ? camData.maxFilmbackWidth : '',
    maxFilmbackHeight: camData?.maxFilmbackHeight ? camData.maxFilmbackHeight : '',
    maxImageWidth: camData?.maxImageWidth ? camData.maxImageWidth : '',
    maxImageHeight: camData?.maxImageHeight ? camData.maxImageHeight : '',
    minFrameRate: camData?.minFrameRate ? camData.minFrameRate : '',
    maxFrameRate: camData?.maxFrameRate ? camData.maxFrameRate : '',
    notes: camData?.notes ? camData.notes : '',
    discontinued: camData?.discontinued ? camData.discontinued : false,
  };

  // Manage the form inputs
  const [cameraFormData, setCameraFormData] = useState(INITIAL_STATE);

  const handleChange = (evt) => {
    const { name, value, files, type, checked } = evt.target;
    if (name === 'image') {
      setCameraFormData((originalData) => ({
        ...originalData,
        image: files[0],
      }));
    } else {
      setCameraFormData((originalData) => ({
        ...originalData,
        [name]: type === 'checkbox' ? checked : value,
      }));
    }
  };

  const handleSubmit = async (evt) => {
    evt.preventDefault();
    onSubmit(cameraFormData);
  };

  return (
    <Form onSubmit={handleSubmit}>
      <Form.Group className="mb-3" controlId="model">
        <Form.Label>Model</Form.Label>
        <Form.Control placeholder="Model" name="model" onChange={handleChange} value={cameraFormData.model} />
      </Form.Group>
      <Form.Group className="mb-3" controlId="sensorType">
        <Form.Label>Sensor Type</Form.Label>
        <Form.Control placeholder="Sensor Type" name="sensorType" onChange={handleChange} value={cameraFormData.sensorType} />
      </Form.Group>
      <Form.Group className="mb-3" controlId="maxFilmbackWidth">
        <Form.Label>Max Filmback Width</Form.Label>
        <Form.Control placeholder="Max Filmback Width" name="maxFilmbackWidth" onChange={handleChange} value={cameraFormData.maxFilmbackWidth} />
      </Form.Group>
      <Form.Group className="mb-3" controlId="maxFilmbackHeight">
        <Form.Label>Max Filmback Height</Form.Label>
        <Form.Control placeholder="Max Filmback Height" name="maxFilmbackHeight" onChange={handleChange} value={cameraFormData.maxFilmbackHeight} />
      </Form.Group>
      <Form.Group className="mb-3" controlId="maxImageWidth">
        <Form.Label>Max Image Width</Form.Label>
        <Form.Control placeholder="Max Image Width" name="maxImageWidth" onChange={handleChange} value={cameraFormData.maxImageWidth} />
      </Form.Group>
      <Form.Group className="mb-3" controlId="maxImageHeight">
        <Form.Label>Max Image Height</Form.Label>
        <Form.Control placeholder="Max Image Height" name="maxImageHeight" onChange={handleChange} value={cameraFormData.maxImageHeight} />
      </Form.Group>
      <Form.Group className="mb-3" controlId="minFrameRate">
        <Form.Label>Min Frame Rate</Form.Label>
        <Form.Control placeholder="Min Frame Rate" name="minFrameRate" onChange={handleChange} value={cameraFormData.minFrameRate} />
      </Form.Group>
      <Form.Group className="mb-3" controlId="maxFrameRate">
        <Form.Label>Max Frame Rate</Form.Label>
        <Form.Control placeholder="Max Frame Rate" name="maxFrameRate" onChange={handleChange} value={cameraFormData.maxFrameRate} />
      </Form.Group>
      <Form.Group className="mb-3" controlId="notes">
        <Form.Label>Notes</Form.Label>
        <Form.Control placeholder="Notes" name="notes" onChange={handleChange} value={cameraFormData.notes} />
      </Form.Group>
      <Form.Check type="switch" className="mb-3" id="discontinued" name="discontinued" label="Discontinued?" onChange={handleChange} checked={cameraFormData.discontinued} />
      <Form.Group className="mb-3" controlId="image">
        <Form.Label>Thumbmail</Form.Label>
        <Form.Control type="file" name="image" onChange={handleChange} />
      </Form.Group>
      <Button type="submit" className="w-100">
        {buttonLabel}
      </Button>
    </Form>
  );
};

export default CameraForm;
