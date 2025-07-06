import ProjectRow from './ProjectRow';
import { Table } from 'react-bootstrap';

const ProjectList = ({ projects }) => {
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
          return <ProjectRow project={project} key={project.id} />;
        })}
      </tbody>
    </Table>
  );
};

export default ProjectList;
