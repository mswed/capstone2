import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { Container, Card, Row, Col } from 'react-bootstrap';
import GrumpyApi from '../../services/api';
import Loading from '../../components/ui/Loading';
import CameraList from '../../features/cameras/components/CameraList';
import ActionBar from '../../components/ui/ActionBar.jsx';
import ModalWindow from '../../components/ui/ModalWindow.jsx';
import MakeForm from '../../components/forms/MakeForm.jsx';
import ConfirmDialog from '../../components/ui/ConfirmDialog.jsx';

const MakeDetails = () => {
  const navigate = useNavigate();

  const { makeId } = useParams();
  const [makeData, setMakeData] = useState(null);
  const [showEditModal, setShowEditModal] = useState(false);
  const [showConfirmDelete, setConfirmDelete] = useState(false);
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
      onClick: () => console.log('adding a camera'),
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
        title="Are you sure?"
        message={`Delete make ${makeData.name}?`}
        confirmText="Delete"
        onConfirm={handleDeleteMake}
        onCancel={() => setConfirmDelete(false)}
      />
      <ModalWindow
        show={showEditModal}
        onHide={() => setShowEditModal(false)}
        title={`Edit ${makeData.name}`}
        form={<MakeForm onSubmit={handleEditMake} makeData={makeData} />}
        onFormSubmit={handleEditMake}
      />
      <Row className="mt-3">
        <CameraList cameras={makeData.cameras} />
      </Row>
    </Container>
  );
};

export default MakeDetails;
