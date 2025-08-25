import { useState, useEffect } from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import GrumpyApi from '../services/api';

const Home = () => {
  const [stats, setStats] = useState({});

  useEffect(() => {
    async function getStats() {
      try {
        const res = await GrumpyApi.getStats();
        setStats(res);
      } catch (error) {
        console.error('Error fetching stats', error);
      }
    }
    getStats();
  }, []);

  return (
    <Container className="mt-3">
      <Row>
        <Col>
          <div
            style={{
              backgroundImage: 'url("/home.png")',
              backgroundSize: 'cover',
              backgroundPosition: 'center',
              backgroundRepeat: 'no-repeat',
              minHeight: '400px',
              position: 'relative',
              color: 'white',
              textShadow: '2px 2px 4px rgba(0, 0, 0, 0.8)',
            }}
          >
            <h3 style={{ position: 'absolute', top: '20px', left: '20px' }}>{stats.projects} Projects</h3>

            <h3 style={{ position: 'absolute', top: '80px', left: '120px' }}>{stats.makes} Makes</h3>

            <h3 style={{ position: 'absolute', top: '160px', left: '200px' }}>{stats.cameras} Cameras</h3>

            <h3 style={{ position: 'absolute', top: '240px', left: '280px' }}>{stats.formats} Formats</h3>

            <h3 style={{ position: 'absolute', top: '320px', left: '360px' }}>Endless complaints...</h3>
          </div>
        </Col>
      </Row>
    </Container>
  );
};

export default Home;
