import { useState, useEffect } from 'react';
import { Container, Card, Row, Col } from 'react-bootstrap';
import GrumpyApi from '../../services/api';
import Loading from '../../components/ui/Loading';
import RemoteSearchForm from '../../components/forms/RemoteSearchForm';
import SourceList from '../../features/sources/SourceList';
import useSources from '../../hooks/useSources';

const Sources = () => {
  const { sources, setSources, isLoading } = useSources();
  const [searchTerm, setSearchTerm] = useState('');
  // We need to check if we're still loading so we won't run into trying to
  // render a null state

  if (isLoading) {
    return <Loading />;
  }
  return (
    <Container>
      <SourceList sources={sources} />
    </Container>
  );
};

export default Sources;
