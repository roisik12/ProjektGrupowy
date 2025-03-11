# 🌍 ProjektGrupowy – Monitorowanie Jakości Powietrza  

Aplikacja webowa i mobilna umożliwiająca **sprawdzanie jakości powietrza** w wybranych lokalizacjach.  
Pobiera dane z **Google Firestore**, a w przyszłości wykorzysta **AI do prognozowania zmian jakości powietrza**.  

---

## 🚀 Technologie  
### 🔹 Backend (Mikroserwisy)  
- **FastAPI** – szybkie API w Pythonie  
- **Google Firestore** – baza danych NoSQL w chmurze  
- **Uvicorn** – serwer ASGI do FastAPI  
- **Pydantic** – walidacja danych w FastAPI  
- **Logging** – monitorowanie działania aplikacji  

### 🔹 Frontend *(do implementacji)*  
- **React.js** – aplikacja webowa  
- **TailwindCSS** – stylowanie interfejsu  
- **Axios** – pobieranie danych z API  

### 🔹 Chmura i Hosting  
- **Google Cloud Platform (GCP)**  
  - **Cloud Firestore** – przechowywanie danych  
  - **Cloud Run** – hostowanie mikroserwisów  
  - **API Gateway** – zarządzanie ruchem API  

---

## ⚙️ Funkcjonalności  
✅ **Sprawdzanie aktualnej jakości powietrza** w danym mieście (AQI)  
✅ **Dodawanie i przechowywanie danych w Firestore**  
✅ **Usuwanie danych o jakości powietrza**  
✅ **Walidacja danych** (AQI: 0-500)  
✅ **Logowanie API dla lepszej kontroli błędów**  

📌 **Planowane funkcjonalności**:  
🔜 **Prognozowanie jakości powietrza** na podstawie historycznych danych (AI)  
🔜 **Integracja z zewnętrznymi API o jakości powietrza**  
🔜 **Aplikacja mobilna React Native**  

---

## 🛠 Instrukcja uruchomienia backendu  
### 1️⃣ Klonowanie repozytorium  
```bash
git clone https://github.com/TwojeRepozytorium/ProjektGrupowy.git
cd ProjektGrupowy
```
### 2️⃣ Tworzenie środowiska wirtualnego  
```bash
python3 -m venv venv
source venv/bin/activate  # (Linux/macOS)
venv\Scripts\activate  # (Windows
```
### 3️⃣ Instalacja zależności
```bash
pip install -r requirements.txt
```
### 4️⃣ Konfiguracja Firestore
Pobierz klucz JSON do Firestore (firestore_key.json)
Umieść go w folderze backend/
Nie commituj pliku! Dodaj go do .gitignore
```
### 5️⃣ Uruchomienie mikroserwisu air-quality-service
```bash
cd backend
uvicorn air_quality_service.main:app --host 0.0.0.0 --port 8001 --reload
```
###📌 Testowanie:
Swagger UI: http://127.0.0.1:8001/docs
Sprawdzenie jakości powietrza:
```bash
curl -X GET "http://127.0.0.1:8001/air-quality/Warsaw"
```

### 👨‍💻 Autorzy
Maciej Łapiński

Maksymilian Wyszatycki

Filip Pławiński

