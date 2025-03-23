import React, { createContext, useState, useEffect, useContext } from 'react';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(sessionStorage.getItem('token'));
  const [userRole, setUserRole] = useState(sessionStorage.getItem('userRole'));

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
            sessionStorage.setItem('userRole', userData.role);
          } else {
            setToken(null);
            setUserRole(null);
            sessionStorage.removeItem('token');
            sessionStorage.removeItem('userRole');
          }
        } catch (error) {
          console.error('Token verification failed:', error);
          setToken(null);
          setUserRole(null);
          sessionStorage.removeItem('token');
          sessionStorage.removeItem('userRole');
        }
      }
    };

    verifyToken();
  }, [token]);

  const login = (newToken, role) => {
    sessionStorage.setItem('token', newToken);
    sessionStorage.setItem('userRole', role);
    setToken(newToken);
    setUserRole(role);
  };

  const logout = () => {
    sessionStorage.removeItem('token');
    sessionStorage.removeItem('userRole');
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