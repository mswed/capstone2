import { useState, useEffect } from 'react';
import { Container, Card, Row, Col, Button } from 'react-bootstrap';
import GrumpyApi from '../../services/api';
import Loading from '../../components/ui/Loading';
import AdvanceSearchForm from '../../components/forms/AdvanceSearchForm';
import FormatList from '../../features/formats/components/FormatList';

const Formats = () => {
  const [formats, setFormats] = useState([]);
  const [formatCount, setFormatCount] = useState(0);
  const [searchParams, setSearchParams] = useState({});
  // We need to check if we're still loading so we won't run into trying to
  // render a null state
  const [isLoading, setIsLoading] = useState(true);

  /**
   * Get all the formats in the database. Eventually this should have a limit
   * or pagination but for now we get everything. This is called by useEffect
   * if the searchPArams changes and is empty
   *
   * @returns {Array} all cameras in the database
   */

  const getAllFormats = async () => {
    try {
      const response = await GrumpyApi.getFormats();
      setFormats(response);
    } catch (error) {
      console.error('Error fetching cameras', error);
    } finally {
      setIsLoading(false);
    }
  };

  /**
   * Get found formats in the databse. This is called by useEffect
   * if the searchParams changes and is NOT empty
   *
   * @returns {Array} found cameras in the database
   */

  const findFormats = async () => {
    try {
      const response = await GrumpyApi.findFormats(searchParams);
      setFormats(response);
    } catch (error) {
      console.error('Error fetching cameras', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleClearSearch = () => {
    setSearchParams([]);
  };
  useEffect(() => {
    if (Object.keys(searchParams).length !== 0) {
      findFormats();
    } else {
      getAllFormats();
    }
    window.scrollTo(0, 0);
  }, [searchParams]);

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
