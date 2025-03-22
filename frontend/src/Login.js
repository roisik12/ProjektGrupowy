import React, { useState } from "react";
import {
  auth,
  provider,
  signInWithPopup,
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
} from "./firebase";
import { useNavigate } from "react-router-dom";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const fetchUserRole = async (idToken) => {
    try {
        const res = await fetch("http://localhost:8001/me", {
            headers: {
                Authorization: `Bearer ${idToken}`,
            },
        });
        const data = await res.json();
        console.log("Dane z backendu:", data); // Dodaj logowanie
        return data.role; // Pobieramy rolę
    } catch (err) {
        console.error("❌ Błąd pobierania roli:", err);
        return null;
    }
};

  const handleGoogleLogin = async () => {
    try {
      const result = await signInWithPopup(auth, provider);
      const idToken = await result.user.getIdToken();

      if (!idToken) {
        console.warn("❌ Nie zalogowano – brak tokenu.");
        return;
      }

      // Pobierz rolę użytkownika z backendu
      const role = await fetchUserRole(idToken);

      // Przekierowanie na podstawie roli
      if (role === "admin") {
        navigate("/admin");
      } else {
        navigate("/guest");
      }
    } catch (err) {
      console.error("❌ Błąd logowania Google:", err);
    }
  };

  const handleEmailLogin = async () => {
    try {
      const result = await signInWithEmailAndPassword(auth, email, password);
      const idToken = await result.user.getIdToken();

      if (!idToken) {
        console.warn("❌ Nie zalogowano – brak tokenu.");
        return;
      }

      // Pobierz rolę użytkownika z backendu
      const role = await fetchUserRole(idToken);

      // Przekierowanie na podstawie roli
      if (role === "admin") {
        navigate("/admin");
      } else {
        navigate("/guest");
      }
    } catch (err) {
      alert("Błędny e-mail lub hasło");
      console.error("❌ Błąd logowania e-mail:", err);
    }
  };

  const handleRegister = async () => {
    try {
      const result = await createUserWithEmailAndPassword(auth, email, password);
      const idToken = await result.user.getIdToken();

      if (!idToken) {
        console.warn("❌ Nie zalogowano – brak tokenu.");
        return;
      }

      // Pobierz rolę użytkownika z backendu
      const role = await fetchUserRole(idToken);

      // Przekierowanie na podstawie roli
      if (role === "admin") {
        navigate("/admin");
      } else {
        navigate("/guest");
      }
    } catch (err) {
      alert("Nie udało się zarejestrować: " + err.message);
      console.error("❌ Błąd rejestracji:", err);
    }
  };

  return (
    <div>
      <h2>Zaloguj się / Zarejestruj</h2>

      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      /><br />

      <input
        type="password"
        placeholder="Hasło"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      /><br />

      <button onClick={handleEmailLogin}>Zaloguj e-mailem</button>
      <button onClick={handleRegister}>Zarejestruj</button>

      <hr />

      <button onClick={handleGoogleLogin}>Zaloguj przez Google</button>
    </div>
  );
};

export default Login;
