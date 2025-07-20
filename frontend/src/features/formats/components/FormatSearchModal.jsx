import { Col, Container, Modal, Row } from 'react-bootstrap';
import Loading from '../../../components/ui/Loading';
import FormatList from './FormatList';
import AdvanceSearchForm from '../../../components/forms/AdvanceSearchForm';
import useFormatSearch from '../../../hooks/useFormatSearch.js';

const FormatSearchModal = ({ show, onHide, onFormatSelect, projectId }) => {
  const { formats, searchParams, setSearchParams, isLoading } = useFormatSearch();

  const handleFormatAdd = async (formatId) => {
    try {
      await onFormatSelect(formatId);
    } catch (error) {
      console.error('Error adding format to project:', error);
    }
  };

  return (
    <Modal show={show} onHide={onHide} size="xl" centered>
      <Modal.Header closeButton>
        <Modal.Title>Add Format To Project</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Container fluid>
          <Row>
            <Col lg={8} md={7}>
              {isLoading ? <Loading /> : <FormatList formats={formats} showModel={true} showAddButton={true} onFormatAdd={handleFormatAdd} />}
            </Col>
            <Col lg={4} md={3}>
              <AdvanceSearchForm search={setSearchParams} />
            </Col>
          </Row>
        </Container>
      </Modal.Body>
    </Modal>
  );
};

export default FormatSearchModal;
