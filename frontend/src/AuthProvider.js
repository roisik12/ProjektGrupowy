import React, { createContext, useState, useEffect, useContext } from 'react';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(sessionStorage.getItem('token'));
  const [userRole, setUserRole] = useState(sessionStorage.getItem('userRole'));

  const [userEmail, setUserEmail] = useState(sessionStorage.getItem('userEmail'));

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
            setUserEmail(userData.email); // <- dodatkowo ustawiamy email z backendu jeśli chcesz
            sessionStorage.setItem('userRole', userData.role);
            if (userData.email) {
              sessionStorage.setItem('userEmail', userData.email);
            }
          } else {
            clearSession();
          }
        } catch (error) {
          console.error('Token verification failed:', error);
          clearSession();

        }
      }
    };

    verifyToken();
  }, [token]);
  const login = (newToken, role, email) => {
    sessionStorage.setItem('token', newToken);
    sessionStorage.setItem('userRole', role);
    if (email) {
      sessionStorage.setItem('userEmail', email);
      setUserEmail(email);
    }
    setToken(newToken);
    setUserRole(role);
  };

  const logout = () => {
    clearSession();
  };

  const clearSession = () => {
    sessionStorage.removeItem('token');
    sessionStorage.removeItem('userRole');
    sessionStorage.removeItem('userEmail');
    setToken(null);
    setUserRole(null);
    setUserEmail(null);
  };

  return (
    <AuthContext.Provider value={{ token, userRole, userEmail, login, logout }}>

      {children}
    </AuthContext.Provider>
  );
};
export const useAuth = () => useContext(AuthContext);

