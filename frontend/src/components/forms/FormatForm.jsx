import { Form, Button } from 'react-bootstrap';
import { useState, useContext } from 'react';
import ModalWindow from '../ui/ModalWindow';
import SourceForm from './SourceForm';

const FormatForm = ({ onSubmit, formatData, sources, onSourceAdded }) => {
  const INITIAL_STATE = {
    source: '',
    imageFormat: '',
    imageAspect: '',
    formatName: '',
    sensorWidth: '',
    imageWidth: '',
    imageHeight: '',
    sensorHeight: '',
    isAnamorphic: false,
    anamorphicSqueeze: 1.0,
    isDesqueezed: false,
    pixelAspect: 1.0,
    isDownsampled: false,
    isUpscaled: false,
    codec: '',
    rawRecordingAvailable: true,
    notes: '',
    makeNotes: '',
  };

  // Manage the form inputs
  const [formatFormData, setFormatFormData] = useState(INITIAL_STATE);
  const [showNewSourceModal, setShowNewSourceModal] = useState(false);

  const handleChange = (evt) => {
    const { name, value, type, checked } = evt.target;
    setFormatFormData((originalData) => ({
      ...originalData,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  const handleSubmit = async (evt) => {
    evt.preventDefault();
    onSubmit(formatFormData);
  };

  const handleSourceAdded = async (sourceData) => {
    // Add source on paret component
    const newSource = await onSourceAdded(sourceData);

    // Select our new source in the list
    setFormatFormData((prev) => ({
      ...prev,
      source: newSource.id,
    }));

    setShowNewSourceModal(false);
  };

  return (
    <>
      <ModalWindow
        show={showNewSourceModal}
        onHide={() => setShowNewSourceModal(false)}
        title={`Add source to format ${formatFormData.imageFormat} ${formatFormData.imageAspect} ${formatFormData.formatName}`}
        form={<SourceForm onSubmit={handleSourceAdded} />}
      />
      <Form onSubmit={handleSubmit}>
        <Form.Group className="mb-3" controlId="source">
          <div className="d-flex justify-content-between align-items-center mb-2">
            <Form.Label className="mb-0">Source</Form.Label>
            <Button variant="outline-success" size="sm" onClick={() => setShowNewSourceModal(true)}>
              Add Source
            </Button>
          </div>
          <Form.Select name="source" value={formatFormData.source} onChange={handleChange}>
            <option value="">Select a source</option>
            {sources.map((source) => (
              <option key={source.id} value={source.id}>
                {source.name}
              </option>
            ))}
          </Form.Select>
        </Form.Group>
        <Form.Group className="mb-3" controlId="imageFormat">
          <Form.Label>Image Format</Form.Label>
          <Form.Control placeholder="Image Format" name="imageFormat" onChange={handleChange} value={formatFormData.imageFormat} />
        </Form.Group>
        <Form.Group className="mb-3" controlId="imageAspect">
          <Form.Label>Image Aspect</Form.Label>
          <Form.Control placeholder="Image Aspect" name="imageAspect" onChange={handleChange} value={formatFormData.imageAspect} />
        </Form.Group>
        <Form.Group className="mb-3" controlId="formatName">
          <Form.Label>Format Name</Form.Label>
          <Form.Control placeholder="Format Name" name="formatName" onChange={handleChange} value={formatFormData.formatName} />
        </Form.Group>
        <Form.Group className="mb-3" controlId="imageWidth">
          <Form.Label>Image Width</Form.Label>
          <Form.Control placeholder="Image Width" name="imageWidth" onChange={handleChange} value={formatFormData.imageWidth} />
        </Form.Group>
        <Form.Group className="mb-3" controlId="imageHeight">
          <Form.Label>Image Height</Form.Label>
          <Form.Control placeholder="Image Height" name="imageHeight" onChange={handleChange} value={formatFormData.imageHeight} />
        </Form.Group>
        <Form.Group className="mb-3" controlId="sensorWidth">
          <Form.Label>Sensor Width</Form.Label>
          <Form.Control placeholder="Sensor Width" name="sensorWidth" onChange={handleChange} value={formatFormData.sensorWidth} />
        </Form.Group>
        <Form.Group className="mb-3" controlId="sensorHeight">
          <Form.Label>Sensor Height</Form.Label>
          <Form.Control placeholder="Sensor Height" name="sensorHeight" onChange={handleChange} value={formatFormData.sensorHeight} />
        </Form.Group>
        <Form.Check type="switch" className="mb-3" id="isAnamorphic" name="isAnamorphic" label="Anamorphic?" onChange={handleChange} checked={formatFormData.isAnamorphic} />
        <Form.Group className="mb-3" controlId="anamorphicSqueeze">
          <Form.Label>Anamorphic Squeeze</Form.Label>
          <Form.Control placeholder="Anamorphic Squeeze" name="anamorphicSqueeze" onChange={handleChange} value={formatFormData.anamorphicSqueeze} />
        </Form.Group>
        <Form.Check type="switch" className="mb-3" id="isDesqueezed" name="isDesqueezed" label="Desqueezed?" onChange={handleChange} checked={formatFormData.isDesqueezed} />
        <Form.Group className="mb-3" controlId="pixelAspect">
          <Form.Label>Pixel Aspect</Form.Label>
          <Form.Control placeholder="Pixel Aspect" name="pixelAspect" onChange={handleChange} value={formatFormData.pixelAspect} />
        </Form.Group>
        <Form.Check type="switch" className="mb-3" id="isDownsampled" name="isDownsampled" label="Downsampled?" onChange={handleChange} checked={formatFormData.isDownsampled} />
        <Form.Check type="switch" className="mb-3" id="isUpscaled" name="isUpscaled" label="Upscaled?" onChange={handleChange} checked={formatFormData.isUpscaled} />
        <Form.Group className="mb-3" controlId="maxFrameRate">
          <Form.Label>Codec</Form.Label>
          <Form.Control placeholder="Codec" name="codec" onChange={handleChange} value={formatFormData.codec} />
        </Form.Group>
        <Form.Group className="mb-3" controlId="notes">
          <Form.Label>Notes</Form.Label>
          <Form.Control placeholder="Notes" name="notes" onChange={handleChange} value={formatFormData.notes} />
        </Form.Group>
        <Form.Group className="mb-3" controlId="notes">
          <Form.Label>Manufacturer Notes</Form.Label>
          <Form.Control placeholder="Manufacturer Notes" name="makeNotes" onChange={handleChange} value={formatFormData.makeNotes} />
        </Form.Group>
        <Button type="submit" className="w-100">
          Add
        </Button>
      </Form>
    </>
  );
};

export default FormatForm;
