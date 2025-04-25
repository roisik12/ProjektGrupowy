import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from './AuthProvider';

const Unauthorized = () => {
  const navigate = useNavigate();
  const { logout } = useAuth();

  useEffect(() => {
    // If user reaches unauthorized page, log them out and redirect to login
    logout();
    navigate('/login');
  }, [logout, navigate]);

  return null; // No need to render anything as we're redirecting
};

export default Unauthorized;
