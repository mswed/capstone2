import { useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { AuthContext } from './AuthContext';
import { Button } from 'react-bootstrap';
import GrumpyApi from './api';

const ProjectRow = ({ project, rowType = 'local' }) => {
  const { token } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogin = () => {
    navigate('/login');
  };

  const handleAdd = async () => {
    console.log('Adding project', project.id || project.tmdb_id, project.project_type);
    GrumpyApi.addTMDBProject(project.id || project.tmdb_id, project.project_type);
  };

  return (
    <tr>
      <td>
        <img src={project.poster_path ? project.poster_path : '/media/camera_images/missing_image.png'} alt={`Image of ${project.model}`} style={{ width: '60px' }} />
      </td>
      <td>{project.name}</td>
      <td>{project.release_date}</td>
      <td>{project.project_type}</td>
      <td className="text-start">{project.description}</td>
      <td>
        {rowType === 'local' ? (
          <Link to={`/projects/${project.id}`} className="btn btn-outline-primary btn-sm">
            View
          </Link>
        ) : token ? (
          <Button variant="outline-danger" onClick={handleAdd}>
            Add
          </Button>
        ) : (
          <Button variant="outline-warning" onClick={handleLogin}>
            Login to Add
          </Button>
        )}
      </td>
    </tr>
  );
};

export default ProjectRow;
