import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Container, Row, Col } from 'react-bootstrap';
import GrumpyApi from './api.js';
import MakeCard from './MakeCard.jsx';

const MakeList = () => {
  const [makes, setMakes] = useState([]);
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
      <Row className="mt-3">
        {makes.map((make) => (
          <Col key={make.id} xs={12} sm={6} md={4} className="p-3">
            <Link to={`/makes/${make.id}`} className="text-decoration-none">
              <MakeCard name={make.name} logo={make.logo} camCount={make.cameras_count} />
            </Link>
          </Col>
        ))}
      </Row>
    </Container>
  );
};

export default MakeList;
