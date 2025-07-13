import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Container, Card, Row, Col } from 'react-bootstrap';
import GrumpyApi from '../../services/api';
import Loading from '../../components/ui/Loading';
import CameraList from '../../features/cameras/components/CameraList';
import ActionBar from '../../components/ui/ActionBar.jsx';
import ModalWindow from '../../components/ui/ModalWindow.jsx';
import MakeForm from '../../components/forms/MakeForm.jsx';

const MakeDetails = () => {
  const { makeId } = useParams();
  const [makeData, setMakeData] = useState(null);
  const [showEditModal, setShowEditModal] = useState(false);

  // We need to check if we're still loading so we won't run into trying to
  // render a null state
  const [isLoading, setIsLoading] = useState(true);

  const actionButtons = [
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
      console.log('updated make is', updatedMake);
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
