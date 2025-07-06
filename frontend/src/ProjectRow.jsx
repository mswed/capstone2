import { Link } from 'react-router-dom';

const ProjectRow = ({ project }) => {
  console.log('GOT PROJECT', project);
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
        <Link to={`/projects/${project.id}`} className="btn btn-outline-primary btn-sm">
          View
        </Link>
      </td>
    </tr>
  );
};

export default ProjectRow;
