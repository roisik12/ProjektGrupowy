import React, { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(() => sessionStorage.getItem('token') || null);
  const [userRole, setUserRole] = useState(() => sessionStorage.getItem('userRole') || null);
  const [userEmail, setUserEmail] = useState(() => sessionStorage.getItem('userEmail') || null);

  // This effect re-verifies token on load
  useEffect(() => {
    const verify = async () => {
      if (!token) return;

      try {
        const res = await fetch(`${process.env.REACT_APP_API_BASE_URL}/me`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!res.ok) throw new Error('Token invalid');

        const data = await res.json();
        setUserRole(data.role);
        setUserEmail(data.email);
        sessionStorage.setItem('userRole', data.role);
        sessionStorage.setItem('userEmail', data.email);
      } catch (e) {
        logout();
      }
    };

    verify();
  }, [token]);

  const login = (token, role, email) => {
    sessionStorage.setItem('token', token);
    sessionStorage.setItem('userRole', role);
    sessionStorage.setItem('userEmail', email);

    setToken(token);
    setUserRole(role);
    setUserEmail(email);
  };

  const logout = () => {
    sessionStorage.clear();
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
