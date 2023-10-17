import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import '../styles/registerPageStyles.css';

const API_BASE_URL = 'http://127.0.0.1:8000/api/v1'; // Replace with your actual backend API base URL

const RegisterPage = () => {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(`${API_BASE_URL}/register`, {
        username,
        password,
      });
      localStorage.setItem('access_token', response.data.access_token);
      navigate('/me');
    } catch (error) {
      console.error('Registration Error:', error);
    }
  };

  return (
    <div className="register-container">
      <div className="register-form">
        <h2 className="register-header">Join Your App</h2>
        <form onSubmit={handleRegister}>
          <div className="form-group">
            <label htmlFor="username">Username:</label>
            <input
              type="text"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </div>
          <div className="form-group">
            <label htmlFor="password">Password:</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
          <button type="submit">Join Now</button>
        </form>
      </div>
    </div>
  );
};

export default RegisterPage;
