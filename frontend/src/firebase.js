import { initializeApp } from "firebase/app";
import {
  getAuth,
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  GoogleAuthProvider,
  signInWithPopup,
} from "firebase/auth";
import { getFirestore } from "firebase/firestore";
import { firebaseConfig } from './firebaseConfig.template.js';

// Log environment variables during initialization (for debugging)
console.log("Firebase init with API Key prefix:", firebaseConfig.apiKey?.substring(0, 5) + "...");

// 🔌 Inicjalizacja Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const provider = new GoogleAuthProvider();
const db = getFirestore(app);

// 🔁 Funkcja pomocnicza do pobierania tokenu użytkownika
export async function getToken() {
  const user = auth.currentUser;
  if (user) {
    return await user.getIdToken();
  }
  return null;
}

// 📦 Eksporty
export {
  auth,
  provider,
  signInWithPopup,
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  db
};