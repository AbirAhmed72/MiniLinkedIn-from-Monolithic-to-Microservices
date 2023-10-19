import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import LoginPage from './components/LoginPage';
import RegisterPage from './components/RegisterPage';
import HomePage from './components/HomePage';
import './styles/appStyles.css'
const App = () => {
  // const handleLogout = () => {
  //   // Clear the access token from local storage
  //   localStorage.removeItem('access_token');
  // };

  return (
    <Router>
      <div>
        <nav>
          <ul>
            {/* ... (other navigation links) */}
            <li>
              <Link to="/login">Login Here</Link>
            </li>
            <li>
              <Link to="/register">Register Here</Link>
            </li>
            {/* <li>
              <button onClick={handleLogout}>Logout</button>
            </li> */}
          </ul>
        </nav>

        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/me" element={<HomePage />} />
          {/* Add other routes if needed */}
          {/* <Route path="/me" element={<HomePage />} /> */}
        </Routes>
      </div>
    </Router>
  );
};

export default App;
