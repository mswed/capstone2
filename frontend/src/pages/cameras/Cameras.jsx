import { useState, useEffect } from 'react';
import { Container } from 'react-bootstrap';
import GrumpyApi from '../../services/api';
import Loading from '../../components/ui/Loading';
import RemoteSearchForm from '../../components/forms/RemoteSearchForm';
import CameraList from '../../features/cameras/components/CameraList';

const Cameras = () => {
  const [cameras, setCameras] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  // We need to check if we're still loading so we won't run into trying to
  // render a null state
  const [isLoading, setIsLoading] = useState(true);

  /**
   * Get all the cameras in the database. Eventually this should have a limit
   * or pagination but for now we get everything. This is called by useEffect
   * if the searchTerm changes and is empty
   *
   * @returns {Array} all cameras in the database
   */

  const getAllCameras = async () => {
    try {
      const response = await GrumpyApi.getCameras();
      setCameras(response);
    } catch (error) {
      console.error('Error fetching cameras', error);
    } finally {
      setIsLoading(false);
    }
  };

  /**
   * Get found cameras in the databse. This is called by useEffect
   * if the searchTerm changes and is NOT empty
   *
   * @returns {Array} found cameras in the database
   */

  const findCameras = async () => {
    try {
      const response = await GrumpyApi.findCameras(searchTerm);
      setCameras(response);
    } catch (error) {
      console.error('Error fetching cameras', error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    console.log('useEffect was called! Search term is', searchTerm);
    if (searchTerm.trim() !== '') {
      findCameras();
    } else {
      getAllCameras();
    }
  }, [searchTerm]);

  if (isLoading) {
    return <Loading />;
  }
  return (
    <Container>
      <RemoteSearchForm search={setSearchTerm} />
      <CameraList cameras={cameras} showMake={true} />
    </Container>
  );
};

export default Cameras;
