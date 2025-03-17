import React from "react";
import { auth, provider, signInWithPopup } from "./firebase";

const Login = () => {
  const handleLogin = () => {
    signInWithPopup(auth, provider)
      .then((result) => {
        return result.user.getIdToken();
      })
      .then((idToken) => {
        console.log("🔥 Firebase ID Token:", idToken);

        // 🔥 Send token to backend
        fetch("http://127.0.0.1:8001/protected", {
          method: "GET",
          headers: {
            Authorization: `Bearer ${idToken}`,
          },
        })
          .then((res) => res.json())
          .then((data) => console.log("🔒 Backend Response:", data))
          .catch((err) => console.error("Backend Error:", err));
      })
      .catch((error) => console.error("Sign-in error:", error));
  };

  return (
    <div>
      <h1>Google Sign-In</h1>
      <button onClick={handleLogin}>Sign in with Google</button>
    </div>
  );
};

export default Login;
