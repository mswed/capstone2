import { useState, useEffect } from 'react';
import { Container, Card, Row, Col } from 'react-bootstrap';
import GrumpyApi from './api';
import Loading from './Loading';
import RemoteSearchForm from './RemoteSearchForm';
import ProjectList from './ProjectList';
import NoResults from './NoResults';

const Projects = () => {
  const [projects, setProjects] = useState({ local: [], remote: [] });
  const [searchTerm, setSearchTerm] = useState('');
  const [isLoading, setIsLoading] = useState(true);

  // Conditions for rendering
  const hasSearch = searchTerm.trim() !== '';
  const hasLocalResults = projects.local.length > 0;
  const hasRemoteResults = projects.remote.length > 0;

  /**
   * Get all the projects in the database. Eventually this should have a limit
   * or pagination but for now we get everything. This is called by useEffect
   * if the searchTerm changes and is empty
   *
   * @returns {Array} all projects in the database
   */

  const getAllProjects = async () => {
    try {
      const response = await GrumpyApi.getProjects();
      setProjects({ local: response, remote: [] });
    } catch (error) {
      console.error('Error fetching cameras', error);
    } finally {
      setIsLoading(false);
    }
  };

  /**
   * Get found projects in the databse. This is called by useEffect
   * if the searchTerm changes and is NOT empty
   *
   * @returns {Array} found projects in the database
   */

  const findProjects = async () => {
    try {
      const response = await GrumpyApi.findProjects(searchTerm);
      setProjects(response);
      console.log('search set state to', projects);
    } catch (error) {
      console.error('Error fetching projects', error);
    } finally {
      setIsLoading(false);
    }
  };

  /**
   * Add a project from TMDB to the local database
   *
   * @param {integer} projectId - Project id from TMDB
   * @param {string} projectType - Project type (episodic or feature)
   */

  const addProject = async (projectId, projectType) => {
    const newProject = await GrumpyApi.addTMDBProject(projectId, projectType);
    setProjects((prev) => ({
      ...prev,
      local: [...prev.local, newProject.project],
    }));
  };

  useEffect(() => {
    if (searchTerm.trim() !== '') {
      findProjects();
    } else {
      getAllProjects();
    }
  }, [searchTerm]);

  if (isLoading) {
    return <Loading />;
  }
  return (
    <Container>
      <RemoteSearchForm search={setSearchTerm} />
      <div className="mb-4">
        <h3 className="text-start">In Database</h3>
        {hasLocalResults ? (
          <ProjectList projects={projects.local} />
        ) : hasSearch ? (
          <NoResults message="No projects found in the databse" />
        ) : (
          <NoResults message="Please search for projects" />
        )}
      </div>
      {hasSearch && (
        <div>
          <h3 className="text-start">Browse TMDB</h3>{' '}
          {hasRemoteResults ? <ProjectList projects={projects.remote} projectsType="remote" onProjectAdd={addProject} /> : <NoResults message="No results found on TMDB" />}
        </div>
      )}
    </Container>
  );
};

export default Projects;
