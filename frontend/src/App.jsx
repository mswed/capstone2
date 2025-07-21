import { Routes, Route } from 'react-router-dom';
import 'bootstrap-icons/font/bootstrap-icons.css';
import './styles/App.css';
import { AuthProvider } from './context/AuthContext';
import NavBar from './components/layout/NavBar';
import Home from './pages/Home';
import Makes from './pages/makes/Makes';
import MakeDetails from './pages/makes/MakeDetails';
import Cameras from './pages/cameras/Cameras';
import CameraDetails from './pages/cameras/CameraDetails';
import Formats from './pages/formats/Formats';
import FormatDetails from './pages/formats/FormatDetails';
import Sources from './pages/sources/Sources';
import SourcesDetails from './pages/sources/SourceDetails.jsx';
import Projects from './pages/projects/Projects';
import ProjectDetails from './pages/projects/ProjectDetails';
import FormContainer from './components/ui/FormContainer';
import LoginForm from './components/forms/LoginForm';

function App() {
  return (
    <>
      <AuthProvider>
        <NavBar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/makes" element={<Makes />} />
          <Route path="/makes/:makeId" element={<MakeDetails />} />
          <Route path="/cameras/" element={<Cameras />} />
          <Route path="/cameras/:cameraId" element={<CameraDetails />} />
          <Route path="/formats/" element={<Formats />} />
          <Route path="/formats/:formatId" element={<FormatDetails />} />
          <Route path="/sources/" element={<Sources />} />
          <Route path="/sources/:sourceId" element={<SourcesDetails />} />
          <Route path="/projects/" element={<Projects />} />
          <Route path="/projects/:projectId" element={<ProjectDetails />} />
          <Route path="/login" element={<FormContainer FormComponent={LoginForm} />} />
        </Routes>
      </AuthProvider>
    </>
  );
}

export default App;
