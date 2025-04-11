import React from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from './AuthProvider';

const GuestPage = () => {
  const navigate = useNavigate();
  const { logout } = useAuth();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="container fade-in">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h1 className="section-header">👋 Witaj, gościu!</h1>
        <button
          className="btn btn-danger"
          onClick={handleLogout}
        >
          Wyloguj się
        </button>
      </div>

      <div className="card slide-in-up" style={{ marginTop: '1rem' }}>
        <p>To jest przykładowa strona przeznaczona dla użytkownika o roli <code>guest</code>.</p>
      </div>
    </div>
  );
};

export default GuestPage;