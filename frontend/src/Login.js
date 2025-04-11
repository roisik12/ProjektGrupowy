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
  console.log("🔍 API BASE URL:", process.env.REACT_APP_API_BASE_URL);
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
    <div className="w-full max-w-md mx-auto mt-10 p-4 sm:p-6 bg-secondary rounded-lg shadow-custom animate-fade-in">
      <h2 className="text-2xl sm:text-3xl font-bold text-highlight text-center mb-6">
        Zaloguj się / Zarejestruj
      </h2>

      <div className="flex flex-col gap-4">
        <div>
          <label className="block text-sm text-white mb-1">E-mail:</label>
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full p-2 sm:p-3 rounded-lg bg-primary text-white focus:outline-none focus:ring-2 focus:ring-highlight text-sm sm:text-base"
          />
        </div>

        <div>
          <label className="block text-sm text-white mb-1">Hasło:</label>
          <input
            type="password"
            placeholder="Hasło"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full p-2 sm:p-3 rounded-lg bg-primary text-white focus:outline-none focus:ring-2 focus:ring-highlight text-sm sm:text-base"
          />
        </div>

        <div className="flex flex-col gap-2 mt-4">
          <button
            className="text-sm sm:text-base bg-accent hover:bg-blue-600 text-white py-2 px-4 rounded-lg transition duration-300"
            onClick={handleEmailLogin}
          >
            Zaloguj e-mailem
          </button>
          <button
            className="text-sm sm:text-base bg-accent hover:bg-blue-600 text-white py-2 px-4 rounded-lg transition duration-300"
            onClick={handleRegister}
          >
            Zarejestruj
          </button>
        </div>

        <hr className="my-6 border-gray-600" />

        <button
          className="text-sm sm:text-base bg-danger hover:bg-red-700 text-white py-2 px-4 rounded-lg transition duration-300"
          onClick={handleGoogleLogin}
        >
          Zaloguj przez Google
        </button>
      </div>
    </div>
  );
};

export default Login;
