import ProjectRow from './ProjectRow';
import { Table } from 'react-bootstrap';

const ProjectList = ({ projects, projectsType = 'local' }) => {
  return (
    <Table striped hover responsive>
      <thead>
        <tr>
          <th>Image</th>
          <th>Name</th>
          <th>Release Date</th>
          <th>Type</th>
          <th>Description</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        {projects.map((project) => {
          return <ProjectRow project={project} rowType={projectsType} key={project.id || project.tmdb_id} />;
        })}
      </tbody>
    </Table>
  );
};

export default ProjectList;
