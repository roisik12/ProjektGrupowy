import React, { createContext, useState, useEffect, useContext } from 'react';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(sessionStorage.getItem('token'));
  const [userRole, setUserRole] = useState(sessionStorage.getItem('userRole'));
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  const clearAuth = () => {
    setToken(null);
    setUserRole(null);
    setError(null);
    sessionStorage.removeItem('token');
    sessionStorage.removeItem('userRole');
  };

  const isTokenExpired = (token) => {
    try {
      const base64Url = token.split('.')[1];
      const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
      const jsonPayload = decodeURIComponent(atob(base64).split('').map((c) => {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
      }).join(''));

      const { exp } = JSON.parse(jsonPayload);
      return exp * 1000 < Date.now();
    } catch (e) {
      return true;
    }
  };

  useEffect(() => {
    const verifyToken = async () => {
      if (!token || isTokenExpired(token)) {
        clearAuth();
        setIsLoading(false);
        return;
      }

      try {
        setIsLoading(true);
        setError(null);
        
        const response = await fetch(`${process.env.REACT_APP_API_BASE_URL}/me`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        
        if (response.ok) {
          const userData = await response.json();
          setUserRole(userData.role);
          sessionStorage.setItem('userRole', userData.role);
        } else {
          const errorData = await response.json();
          setError(errorData.detail || 'Authentication failed');
          clearAuth();
        }
      } catch (error) {
        console.error('Token verification failed:', error);
        setError('Network or server error');
        clearAuth();
      } finally {
        setIsLoading(false);
      }
    };

    verifyToken();
  }, [token]);

  const login = (newToken, role) => {
    if (!newToken || !role) {
      setError('Invalid login credentials');
      return;
    }
    setError(null);
    sessionStorage.setItem('token', newToken);
    sessionStorage.setItem('userRole', role);
    setToken(newToken);
    setUserRole(role);
  };

  const logout = () => {
    clearAuth();
  };

  const getAuthStatus = () => {
    if (isLoading) return 'loading';
    if (error) return 'error';
    if (token && userRole) return 'authenticated';
    return 'unauthenticated';
  };

  const value = {
    token,
    userRole,
    login,
    logout,
    isLoading,
    error,
    authStatus: getAuthStatus()
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};