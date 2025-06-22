import { useState } from 'react';
import { Routes, Route } from 'react-router-dom';
import reactLogo from './assets/react.svg';
import viteLogo from '/vite.svg';
// import './App.css';
import NavBar from './NavBar';
import Home from './Home';
import MakeList from './MakeList';
import MakeDetails from './MakeDetails';
import CameraDetails from './CameraDetails';

function App() {
  const [count, setCount] = useState(0);

  return (
    <>
      <NavBar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/makes" element={<MakeList />} />
        <Route path="/makes/:makeId" element={<MakeDetails />} />
        <Route path="/cameras/:cameraId" element={<CameraDetails />} />
      </Routes>
    </>
  );
}

export default App;
