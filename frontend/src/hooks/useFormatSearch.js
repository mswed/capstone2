import { useState, useEffect } from 'react';
import GrumpyApi from '../services/api.js';

const useFormatSearch = () => {
  const [formats, setFormats] = useState([]);
  const [searchParams, setSearchParams] = useState({});
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
      console.error('Error fetching sources', error);
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

  /**
   * call the api when the search param state changes
   */

  useEffect(() => {
    if (Object.keys(searchParams).length !== 0) {
      findFormats();
    } else {
      getAllFormats();
    }
    window.scrollTo(0, 0);
  }, [searchParams]);

  return {
    formats,
    searchParams,
    setSearchParams,
    isLoading,
  };
};

export default useFormatSearch;
