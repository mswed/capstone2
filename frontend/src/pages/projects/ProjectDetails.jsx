import { useState, useEffect, useContext } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Container, Card, Row, Col } from 'react-bootstrap';
import { AuthContext } from '../../context/AuthContext.jsx';
import GrumpyApi from '../../services/api.js';
import Loading from '../../components/ui/Loading.jsx';
import CameraGrid from '../../features/cameras/components/CamerasGrid.jsx';
import FormatList from '../../features/formats/components/FormatList.jsx';
import ActionBar from '../../components/ui/ActionBar.jsx';
import FormatSearchModal from '../../features/formats/components/FormatSearchModal.jsx';
import ConfirmDialog from '../../components/ui/ConfirmDialog.jsx';

const ProjectDetails = () => {
  // Set up state
  const { projectId } = useParams();
  const [projectData, setProjectData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [showFormatsModal, setShowFormatsModal] = useState(false);
  const [showConfirmDelete, setConfirmDelete] = useState(false);
  const { token, currentUser } = useContext(AuthContext);

  const navigate = useNavigate();

  const actionButtons = [
    {
      text: 'Delete Project',
      variant: 'outline-danger',
      onClick: () => setConfirmDelete(true),
      adminOnly: true,
    },
    {
      text: 'Add Format',
      variant: 'outline-primary',
      onClick: () => setShowFormatsModal(true),
    },
  ];

  const handleAddFormat = async (formatId) => {
    try {
      await GrumpyApi.addFormatToProject(projectId, formatId);
      // Refresh the project
      const response = await GrumpyApi.getProjectDetails(projectId);
      setProjectData(response);
    } catch (error) {}
  };

  const handleVote = async (formatId, vote) => {
    try {
      await GrumpyApi.voteOnProjectFormat(projectId, formatId, vote, currentUser);
      // Refresh the project
      const response = await GrumpyApi.getProjectDetails(projectId);
      setProjectData(response);
    } catch (error) {
      console.error('Error failed to vote on format', error);
    }
  };

  const handleDeleteProject = async () => {
    const response = await GrumpyApi.deleteProject(projectId);
    if (response.success) {
      navigate(-1);
    }
  };

  // Fetch project data
  useEffect(() => {
    const getProjectDetails = async () => {
      try {
        const response = await GrumpyApi.getProjectDetails(projectId);
        setProjectData(response);
      } catch (error) {
        console.error('Error fetching camera details', error);
      } finally {
        setIsLoading(false);
      }
    };
    getProjectDetails();
  }, [projectId]);

  if (isLoading) {
    return <Loading />;
  }

  return (
    <Container>
      <ConfirmDialog
        show={showConfirmDelete}
        title={`Delete project "${projectData.name}"`}
        message={'Are you sure?'}
        confirmText="Delete"
        onConfirm={handleDeleteProject}
        onCancel={() => setConfirmDelete(false)}
      />

      <Card className="shadow-lg rounded-0 rounded-bottom">
        <Row className="g-0">
          <Col md={4}>
            <Card.Img
              src={projectData.posterPath ? projectData.posterPath : '/media/camera_images/missing_image.png'}
              alt={`Poster for for ${projectData.name}`}
              className="p-3"
              style={{
                objectFit: 'contain',
                maxHeight: '350px',
                maxWidth: '100%',
              }}
            />
          </Col>
          <Col md={5}>
            <Card.Body className="text-start">
              <Card.Title>
                <h2>
                  {projectData.name} ({projectData.releaseDate.split('-')[0]})
                </h2>
              </Card.Title>

              <div className="mt-3">
                <h4>Description</h4>
                <p>{projectData.description} </p>
              </div>
              <CameraGrid cameras={projectData.cameras} />
            </Card.Body>
          </Col>
          <Col md={3} className="text-start p-3">
            <div>
              <dl className="row">
                <dt className="col-sm-4">Type:</dt>
                <dd className="col-sm-8">{projectData.projectType}</dd>
              </dl>
            </div>
          </Col>
        </Row>
      </Card>
      {token && <ActionBar buttons={actionButtons} className="mt-3" />}
      <FormatSearchModal show={showFormatsModal} onHide={() => setShowFormatsModal(false)} onFormatSelect={handleAddFormat} projectId={projectId} />
      {projectData.formats?.length > 0 && (
        <Row className="mt-3">
          <div className="text-start">
            <h3>Formats</h3>
          </div>
          <FormatList formats={projectData.formats} showModel={true} onVote={handleVote} />
        </Row>
      )}
    </Container>
  );
};

export default ProjectDetails;
