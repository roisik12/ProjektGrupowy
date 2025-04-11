import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from './AuthProvider';
import TestPanel from "./TestPanel";
import { Navigate } from "react-router-dom";

const AdminPanel = () => {
  const [users, setUsers] = useState([]);
  const navigate = useNavigate();
  const { token, userRole, logout } = useAuth();

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const res = await fetch(`${process.env.REACT_APP_API_BASE_URL}/admin/users`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (res.ok) {
          const data = await res.json();
          setUsers(data);
        } else if (res.status === 401 || res.status === 403) {
          logout();
          navigate('/login');
        }
      } catch (error) {
        console.error('Failed to fetch users:', error);
      }
    };

    if (token && userRole === 'admin') {
      fetchUsers();
    }
  }, [token, userRole, navigate, logout]);

  if (userRole !== 'admin') {
    return <Navigate to="/unauthorized" />;
  }

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h1>Panel administratora</h1>
        <button 
          onClick={handleLogout}
          style={{
            padding: '10px 20px',
            backgroundColor: '#dc3545',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          Wyloguj się
        </button>
      </div>

      <h2>Użytkownicy</h2>
      {users.length > 0 ? (
        <ul>
          {users.map((user) => (
            <li key={user.uid}>
              <span>{user.email} - {user.role}</span>
            </li>
          ))}
        </ul>
      ) : (
        <p>No users found</p>
      )}
      
      <TestPanel />

    </div>
  );
};

export default AdminPanel;
