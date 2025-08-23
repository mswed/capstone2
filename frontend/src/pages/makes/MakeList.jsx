import { useState, useEffect, useContext } from 'react';
import { Link } from 'react-router-dom';
import { Container, Row, Col } from 'react-bootstrap';
import GrumpyApi from '../../services/api.js';
import MakeCard from '../../features/makes/components/MakeCard.jsx';
import ActionBar from '../../components/ui/ActionBar.jsx';
import ModalWindow from '../../components/ui/ModalWindow.jsx';
import MakeForm from '../../components/forms/MakeForm.jsx';
import { AuthContext } from '../../context/AuthContext.jsx';

const MakeList = () => {
  const [makes, setMakes] = useState([]);
  const [showAddModal, setShowAddModal] = useState(false);
  const { token } = useContext(AuthContext);

  const actionButtons = [
    {
      text: 'Add Make',
      variant: 'outline-success',
      onClick: () => setShowAddModal(true),
      adminOnly: true,
    },
  ];

  const handleAddMake = async (newMake) => {
    try {
      // Makes take an image as one of their fields so we have to
      // use FormData instead of json
      const formData = new FormData();
      formData.append('name', newMake.name);
      formData.append('website', newMake.website);
      if (newMake.logo) {
        formData.append('logo', newMake.logo);
      }
      await GrumpyApi.addMake(formData);
      // Refresh the project
      const response = await GrumpyApi.getMakes();
      setMakes(response);

      // Close the modal
      setShowAddModal(false);
    } catch (error) {
      console.error('Failed to add make:', error);
    }
  };

  // On first load fetch all of the makes
  useEffect(() => {
    const getAllMakes = async () => {
      const response = await GrumpyApi.getMakes();
      setMakes(response);
    };
    getAllMakes();
  }, []);

  return (
    <Container>
      {token && <ActionBar buttons={actionButtons} className="mt-3" />}
      <ModalWindow show={showAddModal} onHide={() => setShowAddModal(false)} title="Add Make" form={<MakeForm onSubmit={handleAddMake} />} onFormSubmit={handleAddMake} />
      <Row className="mt-3">
        {makes.map((make) => (
          <Col key={make.id} xs={12} sm={6} md={4} className="p-3">
            <Link to={`/makes/${make.id}`} className="text-decoration-none">
              <MakeCard name={make.name} logo={make.logo} camCount={make.camerasCount} />
            </Link>
          </Col>
        ))}
      </Row>
    </Container>
  );
};

export default MakeList;
