import { useState, useEffect, useContext } from 'react';
import { useParams } from 'react-router-dom';
import { Container, Card, Row, Col } from 'react-bootstrap';
import GrumpyApi from '../../services/api';
import Loading from '../../components/ui/Loading';
import Checkmark from '../../components/ui/Checkmark';
import FormatForm from '../../components/forms/FormatForm.jsx';
import ActionBar from '../../components/ui/ActionBar.jsx';
import ConfirmDialog from '../../components/ui/ConfirmDialog.jsx';
import ModalWindow from '../../components/ui/ModalWindow.jsx';
import { AuthContext } from '../../context/AuthContext.jsx';
import { MessageContext } from '../../context/MessageContext.jsx';
import { useNavigate } from 'react-router-dom';
import useSources from '../../hooks/useSources.js';

const FormatDetails = () => {
  const navigate = useNavigate();
  const { showMessage } = useContext(MessageContext);

  // Set up state
  const { formatId } = useParams();
  const [formatData, setFormatData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [showEditFormatModal, setShowEditFormatModal] = useState(false);
  const [showConfirmDelete, setConfirmDelete] = useState(false);
  const { sources, setSources } = useSources();

  const { token } = useContext(AuthContext);

  const actionButtons = [
    {
      text: 'Delete Format',
      variant: 'outline-danger',
      onClick: () => setConfirmDelete(true),
    },
    {
      text: 'Edit Format',
      variant: 'outline-warning',
      onClick: () => setShowEditFormatModal(true),
    },
  ];

  const handleCopy = async (value) => {
    try {
      await navigator.clipboard.writeText(value);
      showMessage('Copied!', 'success');
    } catch (error) {
      showMessage('Faild to copy value!', 'danger');
      consoel.error('Failed to copy:', error);
    }
  };

  const handleUpdateFormat = async (formatData) => {
    try {
      const updatedFormatDetails = await GrumpyApi.updateFormat(formatId, formatData);
      setFormatData((prev) => ({ ...prev, ...updatedFormatDetails }));

      // Close the modal
      setShowEditFormatModal(false);
      showMessage('Updated format', 'success');
    } catch (error) {
      showMessage('Failed to update format', 'danger');
      console.error('Failed to update format:', error);
    }
  };

  // TODO: This code is similar to the code in CameraDetails
  // The two need to be extracted
  const handleAddSource = async (sourceData) => {
    try {
      const newSource = await GrumpyApi.addSource(sourceData);
      setSources((prev) => [...prev, newSource]);

      // Retrun the new source so we can update the UI
      showMessage('Added source', 'success');
      return newSource;
    } catch (error) {
      showMessage('Failed to add source', 'danger');
      console.error('Failed to add source', error);

      throw error;
    }
  };

  const handleDeleteFormat = async () => {
    const response = await GrumpyApi.deleteFormat(formatId);
    if (response.success) {
      navigate(-1);
      showMessage('Deleted format', 'success');
    } else {
      showMessage('Failed to delete format', 'success');
    }
  };

  // Fetch format data
  useEffect(() => {
    const getFormatDetails = async () => {
      try {
        const response = await GrumpyApi.getFormatDetails(formatId);
        setFormatData(response);
      } catch (error) {
        console.error('Error fetching camera details', error);
      } finally {
        setIsLoading(false);
      }
    };
    getFormatDetails();
  }, [formatId]);

  if (isLoading) {
    return <Loading />;
  }

  return (
    <Container>
      <ConfirmDialog
        show={showConfirmDelete}
        title={`Delete format "${formatData.imageFormat} ${formatData.imageAspect} ${formatData.formatName}"`}
        message={'Are you sure?'}
        confirmText="Delete"
        onConfirm={handleDeleteFormat}
        onCancel={() => setConfirmDelete(false)}
      />
      <Card className="shadow-lg rounded-0 rounded-bottom">
        <Row className="g-0">
          <Col md={3}>
            <Card.Img
              src="/film.png"
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
              <Card.Title>
                {formatData.imageFormat} {formatData.imageAspect} {formatData.formatName}
              </Card.Title>
              <div>
                <dl className="row">
                  <dt className="col-sm-4">Make:</dt>
                  <dd className="col-sm-8">{formatData.makeName}</dd>

                  <dt className="col-sm-4">Model:</dt>
                  <dd className="col-sm-8">{formatData.cameraModel}</dd>

                  <dt className="col-sm-4">Resolution:</dt>
                  <dd className="col-sm-8">
                    {formatData.imageWidth} x {formatData.imageHeight}
                  </dd>
                  <dt className="col-sm-4">Filmback:</dt>
                  <dd className="col-sm-8">
                    {formatData.sensorWidth}mm x {formatData.sensorHeight}mm
                  </dd>
                </dl>
              </div>
            </Card.Body>
          </Col>
          <Col md={5} className="text-start p-3">
            <div>
              <dl className="row">
                <dt className="col-sm-4">Anamorphic?:</dt>
                <dd className="col-sm-8">
                  <Checkmark checked={formatData.isAnamorphic} title="anamorphic?" />
                </dd>
                <dt className="col-sm-4">Desqueezed?:</dt>
                <dd className="col-sm-8">
                  <Checkmark checked={formatData.isDesqueezed} title="desqueezed?" />
                </dd>
                <dt className="col-sm-4">Pixel Aspect:</dt>
                <dd className="col-sm-8">{formatData.pixelAspect}</dd>
                <dt className="col-sm-4">Downsampled?:</dt>
                <dd className="col-sm-8">
                  <Checkmark checked={formatData.isDownsampled} title="downsampled?" />
                </dd>
                <dt className="col-sm-4">Upscaled?:</dt>
                <dd className="col-sm-8">
                  <Checkmark checked={formatData.isUpscaled} title="upscaled?" />
                </dd>
                <dt className="col-sm-4">Codec:</dt>
                <dd className="col-sm-8">{formatData.codec}</dd>
                <dt className="col-sm-4">Raw recording available?:</dt>
                <dd className="col-sm-8">
                  <Checkmark checked={formatData.rawRecordingAvailable} title="row recording available?" />
                </dd>
              </dl>
            </div>
          </Col>
        </Row>
      </Card>
      <ModalWindow
        show={showEditFormatModal}
        onHide={() => setShowEditFormatModal(false)}
        title={`Edit format ${formatData.imageFormat} ${formatData.imageAspect} ${formatData.formatName}`}
        form={<FormatForm onSubmit={handleUpdateFormat} formatData={formatData} sources={sources} onSourceAdded={handleAddSource} buttonLabel="Update" />}
      />
      {token && <ActionBar buttons={actionButtons} className="mt-3" />}
      <Row className="mt-3">
        <Col>
          <Card className="shadow-lg">
            <Card.Body className="text-start">
              <Card.Title>Notes</Card.Title>
              <div>
                <dl>
                  {formatData.notes && <dt className="col-sm-4">Notes:</dt>}
                  {formatData.notes && <dd className="col-sm-8">{formatData.notes}</dd>}
                  {formatData.make_notes && <dt className="col-sm-4">Manufacturer Notes:</dt>}
                  {formatData.make_notes && <dd className="col-sm-8">{formatData.makeNotes}</dd>}
                </dl>
              </div>
            </Card.Body>
          </Card>
        </Col>
      </Row>
      <Row className="mt-3">
        <Col md={6}>
          <Card className="shadow-lg">
            <Card.Body className="text-start">
              <Card.Title>3DE Info</Card.Title>
              <div>
                <dl className="row">
                  <dt className="col-sm-4">Filmback Width:</dt>
                  <dd className="col-md-8">
                    {formatData.filmbackWidth3de}mm{' '}
                    <i
                      className="bi bi-copy text-muted ms-3"
                      role="button"
                      style={{ cursor: 'pointer' }}
                      aria-label="Copy"
                      onClick={() => handleCopy(formatData.filmbackWidth3de)}
                    ></i>
                  </dd>
                  <dt className="col-sm-4">Filmback Height:</dt>
                  <dd className="col-md-8">
                    {formatData.filmbackHeight3de}mm{' '}
                    <i
                      className="bi bi-copy text-muted ms-3"
                      role="button"
                      style={{ cursor: 'pointer' }}
                      aria-label="Copy"
                      onClick={() => handleCopy(formatData.filmbackHeight3de)}
                    ></i>
                  </dd>
                  <dt className="col-sm-4">Distortion Model:</dt>
                  <dd className="col-sm-8">{formatData.distortionModel3de}</dd>
                </dl>
              </div>
            </Card.Body>
          </Card>
        </Col>
        <Col md={6}>
          {formatData.tracking_workflow && (
            <Card className="shadow-lg">
              <Card.Body className="text-start">
                <div>
                  <dl className="row">
                    <dt className="col-sm-4">Tracking Workflow:</dt>
                    <dd className="col-sm-8">{formatData.trackingWorkflow}</dd>
                  </dl>
                </div>
              </Card.Body>
            </Card>
          )}
        </Col>
      </Row>
    </Container>
  );
};

export default FormatDetails;
