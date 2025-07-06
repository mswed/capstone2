import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Container, Row, Col } from 'react-bootstrap';
import GrumpyApi from './api.js';
import MakeCard from './MakeCard.jsx';
import CameraCard from './CameraCard.jsx';

const CameraGrid = ({ cameras }) => {
  return (
    <Row>
      {cameras.map((cam) => (
        <Col key={cam.id} xs={12} sm={6} md={4} className="px-3">
          <Link to={`/cameras/${cam.id}`} className="text-decoration-none">
            <CameraCard camera={cam} />
          </Link>
        </Col>
      ))}
    </Row>
  );
};

export default CameraGrid;
