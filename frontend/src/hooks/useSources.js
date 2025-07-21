import { useState, useEffect } from 'react';
import GrumpyApi from '../services/api.js';

const useSources = () => {
  const [sources, setSources] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  /**
   * Get all the sources in the database.
   *
   * @returns {Array} all cameras in the database
   */

  const getAllSources = async () => {
    try {
      const response = await GrumpyApi.getSources();
      setSources(response);
    } catch (error) {
      console.error('Error fetching sources', error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    getAllSources();
  }, []);

  return {
    sources,
    setSources,
    isLoading,
  };
};

export default useSources;
