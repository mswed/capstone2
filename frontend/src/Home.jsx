import { useState, useEffect } from 'react';
import GrumpyApi from './api';

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
    <div>
      <h1>Welcome to the Grumpy Tracker!</h1>
      <h3>{stats.projects} Projects</h3>
      <h3>{stats.makes} Makes</h3>
      <h3>{stats.cameras} Cameras</h3>
      <h3>{stats.formats} Formats</h3>
      <h3>Endless complaints... </h3>
    </div>
  );
};

export default Home;
