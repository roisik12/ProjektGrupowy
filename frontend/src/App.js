import BackgroundScene from "./BackgroundScene";
import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Login from "./Login";
import AdminPanel from "./AdminPanel";
import GuestPage from "./GuestPage";
import Unauthorized from "./Unauthorized";
import { AuthProvider, useAuth } from './AuthProvider';


function AppRoutes() {
  const { userRole } = useAuth();

  console.log('Current userRole:', userRole); // Debug log

  return (
    <Routes>
      <Route 
        path="/" 
        element={
          userRole ? (
            <Navigate to={userRole === 'admin' ? '/admin' : '/guest'} replace />
          ) : (
            <Navigate to="/login" replace />
          )
        } 
      />
      <Route 
        path="/login" 
        element={
          userRole ? (
            <Navigate to={userRole === 'admin' ? '/admin' : '/guest'} replace />
          ) : (
            <Login />
          )
        } 
      />
      <Route
        path="/admin"
        element={
          userRole === 'admin' ? (
            <AdminPanel />
          ) : (
            <Navigate to="/unauthorized" replace />
          )
        }
      />
      <Route
        path="/guest"
        element={
          userRole === 'guest' ? (
            <GuestPage />
          ) : (
            <Navigate to="/unauthorized" replace />
          )
        }
      />
      <Route path="/unauthorized" element={<Unauthorized />} />
      <Route path="/docs*" element={null} /> {/* This bypasses React Router */}
    </Routes>
  );
}

function App() {
  return (
    <Router>
    <AuthProvider>
      <BackgroundScene />
      <AppRoutes />
    </AuthProvider>
  </Router>
  );
}

export default App;