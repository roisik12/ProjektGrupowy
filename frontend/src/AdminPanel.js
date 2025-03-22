import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom"; // do przekierowań
import { getToken } from "./firebase"; // zakładając, że masz tę funkcję w `firebase.js`
import TestPanel from "./TestPanel";

const AdminPanel = () => {
    const [userRole, setUserRole] = useState(null);
    const [users, setUsers] = useState([]); // Dodajemy stan dla użytkowników
    const navigate = useNavigate(); // Hook do przekierowywania
  
    useEffect(() => {
      const checkUserRole = async () => {
        const idToken = await getToken();
        
        const res = await fetch("http://localhost:8001/me", {
          method: "GET",
          headers: {
            Authorization: `Bearer ${idToken}`,
          },
        });
  
        if (res.ok) {
          const data = await res.json();
          const role = data.role; // Pobierz rolę z odpowiedzi
          if (role === "admin") {
            setUserRole("admin"); // Ustaw rolę jako admin
          } else {
            navigate("/unauthorized"); // Przekieruj do strony "Unauthorized"
          }
        } else {
          navigate("/login"); // Jeśli nie udało się pobrać danych użytkownika, przekieruj do logowania
        }
      };
  
      checkUserRole();
    }, [navigate]);
  
    // Zamiast ręcznie przypisywać użytkowników, możemy pobrać listę użytkowników
    useEffect(() => {
      const fetchUsers = async () => {
        const idToken = await getToken();
        const res = await fetch("http://localhost:8001/admin/users", {
          method: "GET",
          headers: {
            Authorization: `Bearer ${idToken}`,
          },
        });
  
        if (res.ok) {
          const data = await res.json();
          setUsers(data); // Przypisujemy dane użytkowników do stanu `users`
        }
      };
  
      fetchUsers();
    }, []);
  
    if (userRole !== "admin") {
      return <div>Loading...</div>; // Możesz dodać spinner lub inne ładowanie
    }

  return (
    <div>
      <h1>Panel administratora</h1>
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

<h2>🔐 Testowanie Protected Endpoints</h2>
      
      {/* Użycie komponentu TestPanel */}
      <TestPanel />

      {/* Możesz dodać inne funkcje admina tutaj */}
    </div>
  );
};

export default AdminPanel;
