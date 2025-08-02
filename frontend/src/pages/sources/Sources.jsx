import { Container } from 'react-bootstrap';
import Loading from '../../components/ui/Loading';
import SourceList from '../../features/sources/SourceList';
import useSources from '../../hooks/useSources';

const Sources = () => {
  const { sources, isLoading } = useSources();

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
