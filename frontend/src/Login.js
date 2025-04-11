import React, { useState } from "react";
import PrivacyPolicy from './PrivacyPolicy';
import {
  auth,
  provider,
  signInWithPopup,
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
} from "./firebase";
import { useNavigate } from "react-router-dom";
import { useAuth } from './AuthProvider';

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [privacyAccepted, setPrivacyAccepted] = useState(
    localStorage.getItem('privacyAccepted') === 'true'
  );
  const navigate = useNavigate();
  const { login } = useAuth();

  const fetchUserRole = async (idToken) => {
    try {
      const res = await fetch(`${process.env.REACT_APP_API_BASE_URL}/me`, {
        headers: {
          Authorization: `Bearer ${idToken}`,
        },
      });
      
      if (res.status === 401) {
        console.error("Unauthorized: Invalid token or token expired");
        return null;
      }
      
      const data = await res.json();
      console.log("Dane z backendu:", data);
      return data.role;
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

      const role = await fetchUserRole(idToken);
      
      if (role) {
        login(idToken, role);
        navigate(role === 'admin' ? '/admin' : '/guest');
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

      const role = await fetchUserRole(idToken);
      
      if (role) {
        login(idToken, role);
        navigate(role === 'admin' ? '/admin' : '/guest');
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

      const role = await fetchUserRole(idToken);

      if (role) {
        login(idToken, role);
        navigate(role === 'admin' ? '/admin' : '/guest');
      }
    } catch (err) {
      alert("Nie udało się zarejestrować: " + err.message);
      console.error("❌ Błąd rejestracji:", err);
    }
  };

  const handlePrivacyAccept = () => {
    localStorage.setItem('privacyAccepted', 'true');
    setPrivacyAccepted(true);
  };

  if (!privacyAccepted) {
    return <PrivacyPolicy onAccept={handlePrivacyAccept} />;
  }

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
