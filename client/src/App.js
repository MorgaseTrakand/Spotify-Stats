import {
  BrowserRouter as Router,
  Routes,
  Route
} from 'react-router-dom';
import './App.css';
import LandingPage from './pages/landingPage';
import React, { useState } from 'react';
import MyContext from './myContext';
import AuthorizedPage from './pages/authorizedPage';

function App() {
  const [accessToken, setAccessToken] = useState('Initial value');

  return (
    <Router>
      <MyContext.Provider value={{ accessToken, setAccessToken }}>
        <div>
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/dashboard" element={<AuthorizedPage />} />
          </Routes>
        </div>
        </MyContext.Provider> 
    </Router>
  );
}

export default App;
