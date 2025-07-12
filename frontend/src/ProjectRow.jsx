import { useContext, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { AuthContext } from './AuthContext';
import { Button } from 'react-bootstrap';
import GrumpyApi from './api';

const ProjectRow = ({ project, rowType = 'local', onProjectAdd }) => {
  const { token } = useContext(AuthContext);
  const navigate = useNavigate();
  const [isAdding, setIsAdding] = useState(false);
  const [isAdded, setIsAdded] = useState(false);

  const handleLogin = () => {
    navigate('/login');
  };

  const handleAdd = async () => {
    setIsAdding(true);
    try {
      const projectId = project.tmdb_id;
      await onProjectAdd(projectId, project.project_type);
      setIsAdded(true);
    } catch (error) {
      console.error('Failed to add project:', error);
    } finally {
      setIsAdding(false);
    }
  };

  const renderActionButton = () => {
    if (rowType === 'local') {
      return (
        <Link to={`/projects/${project.id}`} className="btn btn-outline-primary btn-sm">
          View
        </Link>
      );
    }

    if (!token) {
      return (
        <Button variant="outline-warning" onClick={handleLogin}>
          Login to Add
        </Button>
      );
    }

    if (isAdded) {
      return (
        <Button variant="success" disabled>
          ✓ Added
        </Button>
      );
    }

    return (
      <Button variant="outline-danger" onClick={handleAdd} disabled={isAdding}>
        {isAdding ? 'Adding...' : 'Add'}
      </Button>
    );
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
      <td>{renderActionButton()}</td>
    </tr>
  );
};

export default ProjectRow;
