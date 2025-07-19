import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { Container, Card, Row, Col } from 'react-bootstrap';
import GrumpyApi from '../../services/api';
import Loading from '../../components/ui/Loading';
import CameraList from '../../features/cameras/components/CameraList';
import ActionBar from '../../components/ui/ActionBar.jsx';
import ModalWindow from '../../components/ui/ModalWindow.jsx';
import MakeForm from '../../components/forms/MakeForm.jsx';
import CameraForm from '../../components/forms/CameraForm.jsx';
import ConfirmDialog from '../../components/ui/ConfirmDialog.jsx';

const MakeDetails = () => {
  const navigate = useNavigate();

  const { makeId } = useParams();
  const [makeData, setMakeData] = useState(null);
  const [showEditModal, setShowEditModal] = useState(false);
  const [showConfirmDelete, setConfirmDelete] = useState(false);
  const [showNewCameraModal, setShowNewCameraModal] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  const actionButtons = [
    {
      text: 'Delete Make',
      variant: 'outline-danger',
      onClick: () => setConfirmDelete(true),
    },
    {
      text: 'Edit Make',
      variant: 'outline-warning',
      onClick: () => setShowEditModal(true),
    },
    {
      text: 'Add Camera',
      variant: 'outline-success',
      onClick: () => setShowNewCameraModal(true),
    },
  ];

  const handleEditMake = async (updatedMake) => {
    try {
      // Makes take an image as one of their fields so we have to
      // use FormData instead of json
      const formData = new FormData();
      formData.append('name', updatedMake.name);
      formData.append('website', updatedMake.website);
      if (updatedMake.logo) {
        formData.append('logo', updatedMake.logo);
      }

      const updatedData = await GrumpyApi.updateMake(makeId, formData);
      // Refresh the project
      setMakeData(updatedData);

      // Close the modal
      setShowEditModal(false);
    } catch (error) {
      console.error('Failed to update make:', error);
    }
  };

  const handleDeleteMake = async () => {
    const response = await GrumpyApi.deleteMake(makeId);
    if (response.success) {
      navigate('/makes');
    }
  };

  const handleNewCamera = async (newCamera) => {
    try {
      // Cameras also take an image as one of their fields so we have to
      // use FormData instead of json
      const formData = new FormData();
      formData.append('make', makeId);
      formData.append('model', newCamera.model);
      formData.append('sensor_type', newCamera.sensorType);
      formData.append('max_filmback_width', newCamera.maxFilmbackWidth);
      formData.append('max_filmback_height', newCamera.maxFilmbackHeight);
      formData.append('max_image_width', newCamera.maxImageWidth);
      formData.append('max_image_height', newCamera.maxImageHeight);
      formData.append('min_frame_rate', newCamera.minFrameRate);
      formData.append('max_frame_rate', newCamera.maxFrameRate);
      formData.append('notes', newCamera.notes);
      formData.append('discontinued', newCamera.discontinued);
      if (newCamera.image) {
        formData.append('image', newCamera.image);
      }

      await GrumpyApi.addCamera(formData);

      // Refresh the make
      const response = await GrumpyApi.getMakeDetails(makeId);
      setMakeData(response);

      // Close the modal
      setShowNewCameraModal(false);
    } catch (error) {
      console.error('Failed to update make:', error);
    }
  };

  useEffect(() => {
    const getMakeDetails = async () => {
      try {
        const response = await GrumpyApi.getMakeDetails(makeId);
        setMakeData(response);
      } catch (error) {
        console.error('Error fetching make details', error);
      } finally {
        setIsLoading(false);
      }
    };
    getMakeDetails();
  }, [makeId]);

  if (isLoading) {
    return <Loading />;
  }
  return (
    <Container>
      <Card className="shadow-lg rounded-0 rounded-bottom">
        <Row className="g-0">
          <Col md={4}>
            <Card.Img src={makeData.logo} alt={`Logo for ${makeData.name}`} className="h-100 p-3" style={{ objectFit: 'cover' }} />
          </Col>
          <Col md={8}>
            <Card.Body className="text-start">
              <Card.Title>{makeData.name}</Card.Title>
              <Card.Text>{makeData.website}</Card.Text>
            </Card.Body>
          </Col>
        </Row>
      </Card>
      <ActionBar buttons={actionButtons} className="mt-3" />
      <ConfirmDialog
        show={showConfirmDelete}
        title={`Delete make "${makeData.name}"`}
        message={'Are you sure?'}
        confirmText="Delete"
        onConfirm={handleDeleteMake}
        onCancel={() => setConfirmDelete(false)}
      />
      <ModalWindow show={showEditModal} onHide={() => setShowEditModal(false)} title={`Edit ${makeData.name}`} form={<MakeForm onSubmit={handleEditMake} makeData={makeData} />} />
      <ModalWindow
        show={showNewCameraModal}
        onHide={() => setShowNewCameraModal(false)}
        title={`New Camera By ${makeData.name}`}
        form={<CameraForm onSubmit={handleNewCamera} makeData={makeData} />}
      />
      {makeData.cameras.length > 0 && (
        <Row className="mt-3">
          <CameraList cameras={makeData.cameras} />
        </Row>
      )}
    </Container>
  );
};

export default MakeDetails;
