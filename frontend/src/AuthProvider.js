import React, { createContext, useState, useEffect, useContext } from 'react';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [userRole, setUserRole] = useState(localStorage.getItem('userRole'));

  useEffect(() => {
    const verifyToken = async () => {
      if (token) {
        try {
          const response = await fetch('http://localhost:8001/me', {
            headers: {
              Authorization: `Bearer ${token}`
            }
          });
          
          if (response.ok) {
            const userData = await response.json();
            setUserRole(userData.role);
            localStorage.setItem('userRole', userData.role);
          } else {
            // If token is invalid, clear everything
            setToken(null);
            setUserRole(null);
            localStorage.removeItem('token');
            localStorage.removeItem('userRole');
          }
        } catch (error) {
          console.error('Token verification failed:', error);
          setToken(null);
          setUserRole(null);
          localStorage.removeItem('token');
          localStorage.removeItem('userRole');
        }
      }
    };

    verifyToken();
  }, [token]);

  const login = (newToken, role) => {
    localStorage.setItem('token', newToken);
    localStorage.setItem('userRole', role);
    setToken(newToken);
    setUserRole(role);
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('userRole');
    setToken(null);
    setUserRole(null);
  };

  return (
    <AuthContext.Provider value={{ token, userRole, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);