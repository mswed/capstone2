import { useState } from 'react';
import { Routes, Route } from 'react-router-dom';
import './App.css';
import 'bootstrap-icons/font/bootstrap-icons.css';
import { AuthProvider } from './AuthContext';
import NavBar from './NavBar';
import Home from './Home';
import MakeList from './MakeList';
import MakeDetails from './MakeDetails';
import Cameras from './Cameras';
import CameraDetails from './CameraDetails';
import Formats from './Formats';
import FormatDetails from './FormatDetails';
import Projects from './Projects';
import ProjectDetails from './ProjectDetails';
import FormContainer from './FormContainer';
import LoginForm from './LoginForm';

function App() {
  return (
    <>
      <AuthProvider>
        <NavBar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/makes" element={<MakeList />} />
          <Route path="/makes/:makeId" element={<MakeDetails />} />
          <Route path="/cameras/" element={<Cameras />} />
          <Route path="/cameras/:cameraId" element={<CameraDetails />} />
          <Route path="/formats/" element={<Formats />} />
          <Route path="/formats/:formatId" element={<FormatDetails />} />
          <Route path="/projects/" element={<Projects />} />
          <Route path="/projects/:projectId" element={<ProjectDetails />} />
          <Route path="/login" element={<FormContainer FormComponent={LoginForm} />} />
        </Routes>
      </AuthProvider>
    </>
  );
}

export default App;
