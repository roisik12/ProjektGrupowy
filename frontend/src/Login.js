import React, { useState } from "react";
import {
  auth,
  provider,
  signInWithPopup,
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
} from "./firebase";
import { useNavigate } from "react-router-dom";
import { useAuth } from "./AuthProvider";
import PrivacyPolicy from "./PrivacyPolicy";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [privacyAccepted, setPrivacyAccepted] = useState(
    localStorage.getItem("privacyAccepted") === "true"
  );

  const { login } = useAuth();
  const navigate = useNavigate();

  const handlePrivacyAccept = () => {
    localStorage.setItem("privacyAccepted", "true");
    setPrivacyAccepted(true);
  };

  const fetchUserInfo = async (idToken) => {
    const res = await fetch(`${process.env.REACT_APP_API_BASE_URL}/me`, {
      headers: {
        Authorization: `Bearer ${idToken}`,
      },
    });

    if (!res.ok) throw new Error("Unauthorized");
    return await res.json();
  };

  const handleLogin = async (authFn) => {
    try {
      const result = await authFn();
      const idToken = await result.user.getIdToken();
      const user = await fetchUserInfo(idToken);

      login(idToken, user.role, user.email);
      navigate(user.role === "admin" ? "/admin" : "/guest");
    } catch (err) {
      console.error("❌ Login failed:", err);
      alert("Błąd logowania");
    }
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
            onClick={() =>
              handleLogin(() => signInWithEmailAndPassword(auth, email, password))
            }
          >
            Zaloguj e-mailem
          </button>

          <button
            className="text-sm sm:text-base bg-accent hover:bg-blue-600 text-white py-2 px-4 rounded-lg transition duration-300"
            onClick={() =>
              handleLogin(() => createUserWithEmailAndPassword(auth, email, password))
            }
          >
            Zarejestruj
          </button>
        </div>

        <hr className="my-6 border-gray-600" />

        <button
          className="text-sm sm:text-base bg-danger hover:bg-red-700 text-white py-2 px-4 rounded-lg transition duration-300"
          onClick={() => handleLogin(() => signInWithPopup(auth, provider))}
        >
          Zaloguj przez Google
        </button>
      </div>
    </div>
  );
};

export default Login;
