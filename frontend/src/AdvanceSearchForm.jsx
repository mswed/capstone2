import { useState } from 'react';
import { Form, Button, InputGroup } from 'react-bootstrap';

/**
 * A search form components that runs a setState function provided by
 * the parent component. The parent component is in charge of running the
 * actual search once the search state provided is changed, but this form handles the UI
 * Unlike SimpleSearchForm this UI has multiple fields and widgets
 *
 * @param {function}  search -  The setState function provided by the parent component
 * @returns {Component} - a search form with a search field and a button
 */

const AdvanceSearchForm = ({ search }) => {
  const INITIAL_STATE = {
    make: 'Any',
    camera: 'Any',
    format: '',
    sensor_width: '',
    sensor_height: '',
    image_width: '',
    imageHeight: '',
    is_anamorphic: false,
    is_desqueezed: false,
    pixel_aspect: 1.0,
    is_downsampled: false,
    is_upscaled: false,
  };

  const [formData, setFormData] = useState(INITIAL_STATE);

  const handleChange = (evt) => {
    const { name, value, type, checked } = evt.target;
    setFormData((originalSearchParams) => ({
      ...originalSearchParams,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  const handleClear = () => {
    setFormData(INITIAL_STATE);
    search({});
  };

  const handleSubmit = (evt) => {
    evt.preventDefault();
    const cleanedParams = {};
    Object.keys(formData).forEach((key) => {
      const value = formData[key];
      if (value && value !== '' && value !== 'Any') {
        cleanedParams[key] = value;
      }
    });
    search(cleanedParams);
  };
  return (
    <Form onSubmit={handleSubmit} className="text-start">
      <div className="d-flex justify-content-between align-items-center">
        <h5 className="mb-0">Filter Formats</h5>
        <Button variant="outline-danger" size="sm" className="border-0" onClick={handleClear}>
          X
        </Button>
      </div>
      <Form.Group className="mb-3" controlId="advanceSearchForm.makeInput">
        <Form.Label>Make</Form.Label>
        <Form.Control type="text" name="make" onChange={handleChange} value={formData.make} />
      </Form.Group>
      <Form.Group className="mb-3" controlId="advanceSearchForm.modelInput">
        <Form.Label>Model</Form.Label>
        <Form.Control type="text" name="camera" onChange={handleChange} value={formData.camera} />
      </Form.Group>
      <Form.Group className="mb-3" controlId="advanceSearchForm.formatInput">
        <Form.Label>Format</Form.Label>
        <Form.Control type="text" name="format" onChange={handleChange} value={formData.format} />
      </Form.Group>
      <Form.Group className="mb-3" controlId="advanceSearchForm.sensorWidthInput">
        <Form.Label>Sensor Width</Form.Label>
        <Form.Control type="text" name="sensor_width" onChange={handleChange} value={formData.sensor_width} />
      </Form.Group>
      <Form.Group className="mb-3" controlId="advanceSearchForm.sensorHeightInput">
        <Form.Label>Sensor Height</Form.Label>
        <Form.Control type="text" name="sensor_height" onChange={handleChange} value={formData.sensor_height} />
      </Form.Group>
      <Form.Group className="mb-3" controlId="advanceSearchForm.imageWidthInput">
        <Form.Label>Image Width</Form.Label>
        <Form.Control type="text" name="image_width" onChange={handleChange} value={formData.image_width} />
      </Form.Group>
      <Form.Group className="mb-3" controlId="advanceSearchForm.imageHeightInput">
        <Form.Label>Image Height</Form.Label>
        <Form.Control type="text" name="image_height" onChange={handleChange} value={formData.imageHeight} />
      </Form.Group>
      <Form.Group className="mb-3" controlId="advanceSearchForm.pixelAspectInput">
        <Form.Label>Pixel Aspect</Form.Label>
        <Form.Control type="text" name="pixel_aspect" onChange={handleChange} value={formData.pixel_aspect} />
      </Form.Group>
      <Form.Check type="switch" id="isAnamorphic" name="is_anamorphic" label="Anamorphic?" onChange={handleChange} checked={formData.is_anamorphic} />
      <Form.Check type="switch" id="isDesqueezed" name="is_desqueezed" label="Desqueezed?" onChange={handleChange} checked={formData.is_desqueezed} />
      <Form.Check type="switch" id="isDownsampled" name="is_downsampled" label="Downsampled?" onChange={handleChange} checked={formData.is_downsampled} />
      <Form.Check type="switch" id="isUpscaled" name="is_upscaled" label="Upscaled?" onChange={handleChange} checked={formData.is_upscaled} />
      <Button type="submit" className="btn btn-primary w-100 my-3">
        Search
      </Button>
    </Form>
  );
};

export default AdvanceSearchForm;
