import { useState } from 'react';
import { Routes, Route } from 'react-router-dom';
import './App.css';
import 'bootstrap-icons/font/bootstrap-icons.css';
import NavBar from './NavBar';
import Home from './Home';
import MakeList from './MakeList';
import MakeDetails from './MakeDetails';
import Cameras from './Cameras';
import CameraDetails from './CameraDetails';
import FormatDetails from './FormatDetails';

function App() {
  const [count, setCount] = useState(0);

  return (
    <>
      <NavBar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/makes" element={<MakeList />} />
        <Route path="/makes/:makeId" element={<MakeDetails />} />
        <Route path="/cameras/" element={<Cameras />} />
        <Route path="/cameras/:cameraId" element={<CameraDetails />} />
        <Route path="/formats/:formatId" element={<FormatDetails />} />
      </Routes>
    </>
  );
}

export default App;
