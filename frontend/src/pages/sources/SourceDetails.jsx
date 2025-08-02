import { useState, useEffect, useContext } from 'react';
import { useParams } from 'react-router-dom';
import { Container, Card, Row, Col } from 'react-bootstrap';
import GrumpyApi from '../../services/api';
import Loading from '../../components/ui/Loading';
import SourceForm from '../../components/forms/SourceForm.jsx';
import ActionBar from '../../components/ui/ActionBar.jsx';
import ConfirmDialog from '../../components/ui/ConfirmDialog.jsx';
import ModalWindow from '../../components/ui/ModalWindow.jsx';
import { AuthContext } from '../../context/AuthContext.jsx';
import { useNavigate } from 'react-router-dom';
import { MessageContext } from '../../context/MessageContext.jsx';

const SourceDetails = () => {
  const navigate = useNavigate();
  const { showMessage } = useContext(MessageContext);

  // Set up state
  const { sourceId } = useParams();
  const [sourceData, setSourceData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [showEditSourceModal, setShowEditSourceModal] = useState(false);
  const [showConfirmDelete, setConfirmDelete] = useState(false);

  const { token } = useContext(AuthContext);

  const actionButtons = [
    {
      text: 'Delete Source',
      variant: 'outline-danger',
      onClick: () => setConfirmDelete(true),
      adminOnly: true,
    },
    {
      text: 'Edit Source',
      variant: 'outline-warning',
      onClick: () => setShowEditSourceModal(true),
      adminOnly: true,
    },
  ];

  const handleUpdateSource = async (updatedSourceData) => {
    try {
      const updatedSourceDetails = await GrumpyApi.updateSource(sourceId, updatedSourceData);
      setSourceData((prev) => ({ ...prev, ...updatedSourceDetails }));

      // Close the modal
      setShowEditSourceModal(false);
      showMessage('Updated source', 'success');
    } catch (error) {
      showMessage('Failed to update source', 'danger');
      console.error('Failed to update source:', error);
    }
  };

  const handleDeleteSource = async () => {
    const response = await GrumpyApi.deleteSource(sourceId);
    if (response.success) {
      navigate(-1);
      showMessage('Deleted source', 'success');
    } else {
      showMessage('Failed to delete source', 'danger');
    }
  };

  // Fetch source data
  useEffect(() => {
    const getSourceDetails = async () => {
      try {
        const response = await GrumpyApi.getSourceDetails(sourceId);
        setSourceData(response);
      } catch (error) {
        console.error('Error fetching source details', error);
      } finally {
        setIsLoading(false);
      }
    };
    getSourceDetails();
  }, [sourceId]);

  if (isLoading) {
    return <Loading />;
  }

  return (
    <Container>
      <ConfirmDialog
        show={showConfirmDelete}
        title={`Delete source "${sourceData.name}"`}
        message={'Are you sure?'}
        confirmText="Delete"
        onConfirm={handleDeleteSource}
        onCancel={() => setConfirmDelete(false)}
      />
      <Card className="shadow-lg rounded-0 rounded-bottom">
        <Row className="g-0">
          <Col md={3}>
            <Card.Img
              src="/source.webp"
              alt="Film strip image"
              className="p-3"
              style={{
                objectFit: 'contain',
                maxHeight: '250px',
                maxWidth: '100%',
              }}
            />
          </Col>
          <Col md={4}>
            <Card.Body className="text-start">
              <Card.Title>{sourceData.name}</Card.Title>
              <div>
                <dl className="row">
                  <dt className="col-sm-4">URL:</dt>
                  <dd className="col-sm-8">{sourceData.url}</dd>
                  <dt className="col-sm-4">File Name:</dt>
                  <dd className="col-sm-8">{sourceData.fileName}</dd>
                  <dt className="col-sm-4">Note:</dt>
                  <dd className="col-sm-8">{sourceData.note}</dd>
                </dl>
              </div>
            </Card.Body>
          </Col>
        </Row>
      </Card>
      <ModalWindow
        show={showEditSourceModal}
        onHide={() => setShowEditSourceModal(false)}
        title={`Edit source ${sourceData.name}`}
        form={<SourceForm onSubmit={handleUpdateSource} sourceData={sourceData} />}
      />
      {token && <ActionBar buttons={actionButtons} className="mt-3" />}
    </Container>
  );
};

export default SourceDetails;
