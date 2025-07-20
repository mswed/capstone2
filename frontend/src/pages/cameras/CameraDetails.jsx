import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Container, Card, Row, Col } from 'react-bootstrap';
import GrumpyApi from '../../services/api.js';
import Loading from '../../components/ui/Loading';
import FormatList from '../../features/formats/components/FormatList';
import LocalSearchForm from '../../components/forms/LocalSearchForm';
import ActionBar from '../../components/ui/ActionBar.jsx';
import ModalWindow from '../../components/ui/ModalWindow.jsx';
import CameraForm from '../../components/forms/CameraForm.jsx';
import FormatForm from '../../components/forms/FormatForm.jsx';
import ConfirmDialog from '../../components/ui/ConfirmDialog.jsx';
import useSources from '../../hooks/useSources.js';

const CameraDetails = () => {
  // Set up state
  const { cameraId } = useParams();
  const [cameraData, setCameraData] = useState(null);
  const [formatsData, setFormatsData] = useState([]);
  const [showEditCameraModal, setShowEditCameraModal] = useState(false);
  const [showNewFormatModal, setShowNewFormatModal] = useState(false);
  const [showConfirmDelete, setConfirmDelete] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const { sources, setSources } = useSources();

  const navigate = useNavigate();

  const actionButtons = [
    {
      text: 'Delete Camera',
      variant: 'outline-danger',
      onClick: () => setConfirmDelete(true),
    },
    {
      text: 'Edit Camera',
      variant: 'outline-warning',
      onClick: () => setShowEditCameraModal(true),
    },
    {
      text: 'Add Format',
      variant: 'outline-success',
      onClick: () => setShowNewFormatModal(true),
    },
  ];

  const handleEditCamera = async (updatedCamera) => {
    try {
      // Cameras also take an image as one of their fields so we have to
      // use FormData instead of json
      const formData = new FormData();
      formData.append('make', cameraData.make);
      formData.append('model', updatedCamera.model);
      formData.append('sensor_type', updatedCamera.sensorType);
      formData.append('max_filmback_width', updatedCamera.maxFilmbackWidth);
      formData.append('max_filmback_height', updatedCamera.maxFilmbackHeight);
      formData.append('max_image_width', updatedCamera.maxImageWidth);
      formData.append('max_image_height', updatedCamera.maxImageHeight);
      formData.append('min_frame_rate', updatedCamera.minFrameRate);
      formData.append('max_frame_rate', updatedCamera.maxFrameRate);
      formData.append('notes', updatedCamera.notes);
      formData.append('discontinued', updatedCamera.discontinued);
      if (updatedCamera.image) {
        formData.append('image', updatedCamera.image);
      }

      const updatedCameraDetails = await GrumpyApi.updateCamera(cameraData.id, formData);
      setCameraData((prev) => ({ ...prev, ...updatedCameraDetails }));

      // Close the modal
      setShowEditCameraModal(false);
    } catch (error) {
      console.error('Failed to update camera:', error);
    }
  };

  const handleDeleteCamera = async () => {
    const response = await GrumpyApi.deleteCamera(cameraId);
    if (response.success) {
      navigate(-1);
    }
  };

  const handleAddFormat = async (newFormat) => {
    try {
      newFormat.camera = cameraId;
      await GrumpyApi.addFormat(newFormat);

      // Refresh the camera
      const response = await GrumpyApi.getCameraDetails(cameraId);
      setCameraData(response);
      setFormatsData(response.formats);

      // Close the modal
      setShowNewFormatModal(false);
    } catch (error) {
      console.error('Failed to create format:', error);
    }
  };

  const handleAddSource = async (sourceData) => {
    try {
      const newSource = await GrumpyApi.addSource(sourceData);
      setSources((prev) => [...prev, newSource]);

      // Retrun the new source so we can update the UI
      return newSource;
    } catch (error) {
      console.error('Failed to add source', error);

      throw error;
    }
  };

  // Fetch camera data
  useEffect(() => {
    const getCameraDetails = async () => {
      try {
        const response = await GrumpyApi.getCameraDetails(cameraId);
        setCameraData(response);
        setFormatsData(response.formats);
      } catch (error) {
        console.error('Error fetching camera details', error);
      } finally {
        setIsLoading(false);
      }
    };
    getCameraDetails();
  }, [cameraId]);

  if (isLoading) {
    return <Loading />;
  }

  return (
    <Container>
      <ConfirmDialog
        show={showConfirmDelete}
        title={`Delete camera "${cameraData.model}"`}
        message={'Are you sure?'}
        confirmText="Delete"
        onConfirm={handleDeleteCamera}
        onCancel={() => setConfirmDelete(false)}
      />
      <Card className="shadow-lg rounded-0 rounded-bottom">
        <Row className="g-0">
          <Col md={4}>
            <Card.Img
              src={cameraData.image ? cameraData.image : '/media/camera_images/missing_image.png'}
              alt={`Logo for ${cameraData.model}`}
              className="p-3"
              style={{
                objectFit: 'contain',
                maxHeight: '250px',
                maxWidth: '100%',
              }}
            />
          </Col>
          <Col md={5}>
            <Card.Body className="text-start">
              <Card.Title>{cameraData.model}</Card.Title>
              <dl className="row">
                <dt className="col-sm-4">Make:</dt>
                <dd className="col-sm-8">{cameraData.make_name}</dd>

                <dt className="col-sm-4">Sensor Type:</dt>
                <dd className="col-sm-8">{cameraData.sensorType}</dd>

                <dt className="col-sm-4">Max Filmback:</dt>
                <dd className="col-sm-8">
                  {cameraData.maxFilmbackWidth}mm x {cameraData.maxFilmbackHeight}mm
                </dd>

                <dt className="col-sm-4">Max Resolution:</dt>
                <dd className="col-sm-8">
                  {cameraData.maxImageWidth} x {cameraData.maxImageHeight}
                </dd>

                <dt className="col-sm-4">Frame Rate:</dt>
                <dd className="col-sm-8">
                  {cameraData.minFrameRate}fps - {cameraData.maxFrameRate}
                  fps
                </dd>
              </dl>
            </Card.Body>
          </Col>
          <Col md={3} className="text-start p-3">
            {cameraData.notes && (
              <div>
                <h6>Notes</h6>
                <p>{cameraData.notes}</p>
              </div>
            )}
          </Col>
        </Row>
      </Card>
      <ActionBar buttons={actionButtons} className="mt-3" />
      <ModalWindow
        show={showEditCameraModal}
        onHide={() => setShowEditCameraModal(false)}
        title={`Edit ${cameraData.makeName} ${cameraData.model}`}
        form={<CameraForm onSubmit={handleEditCamera} camData={cameraData} buttonLabel="Update" />}
      />
      <ModalWindow
        show={showNewFormatModal}
        onHide={() => setShowNewFormatModal(false)}
        title={`Add format to ${cameraData.make_name} ${cameraData.model}`}
        form={<FormatForm onSubmit={handleAddFormat} camData={cameraData} sources={sources} onSourceAdded={handleAddSource} />}
      />
      {cameraData.formats.length > 0 && (
        <Row className="mt-3">
          <Col>
            <Row>
              <LocalSearchForm fields={['imageFormat', 'imageAspect', 'formatName']} targetArray={formatsData} setTargetArray={setFormatsData} originalArray={cameraData.formats} />
            </Row>
            <Row>
              <FormatList formats={formatsData} />
            </Row>
          </Col>
        </Row>
      )}
    </Container>
  );
};

export default CameraDetails;
