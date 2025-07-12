import { useState, useEffect } from 'react';
import { Container, Card, Row, Col, Button } from 'react-bootstrap';
import GrumpyApi from '../../services/api';
import Loading from '../../components/ui/Loading';
import useFormatSearch from '../../features/formats/hooks/useFormatSearch';
import AdvanceSearchForm from '../../components/forms/AdvanceSearchForm';
import FormatList from '../../features/formats/components/FormatList';

const Formats = () => {
  const { formats, searchParams, setSearchParams, isLoading } = useFormatSearch();
  const [formatCount, setFormatCount] = useState(0);

  const handleClearSearch = () => {
    setSearchParams([]);
  };

  useEffect(() => {
    async function getFormatCount() {
      try {
        const res = await GrumpyApi.getStats();
        setFormatCount(res.formats);
      } catch (error) {
        console.error('Error fetching stats', error);
      }
    }
    getFormatCount();
  }, []);

  if (isLoading) {
    return <Loading />;
  }
  return (
    <Container>
      <Row>
        <Col md={9}>
          <FormatList formats={formats} showModel={true} />
          <Row>
            <div className="text-muted text-center">Showing {formats.length} formats</div>
          </Row>
          {formatCount !== formats.length && (
            <Row className="mt-4">
              <Button variant="outline-danger" onClick={handleClearSearch}>
                Clear
              </Button>
            </Row>
          )}
        </Col>
        <Col md={3}>
          <Card className="m-3 px-3 shadow-lg">
            <AdvanceSearchForm search={setSearchParams} />
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default Formats;
