import { useState, useEffect } from 'react';
import GrumpyApi from './api.js';

const MakeList = () => {
  const [makes, setMakes] = useState({});
  // On first load fetch all of the makes
  useEffect(() => {
    const getAllMakes = async () => {
      const response = await GrumpyApi.getMakes();
      setMakes(response.data);
    };
    getAllMakes();
  }, []);
  return <div>MakesList</div>;
};

export default MakeList;
