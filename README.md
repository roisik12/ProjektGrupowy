# 🌍 ProjektGrupowy – Monitorowanie Jakości Powietrza  

Aplikacja webowa umożliwiająca **sprawdzanie jakości powietrza** w wybranych lokalizacjach.  
Dane pobierane są z **Google Firestore**, a w przyszłości wykorzystamy **AI do prognozowania zmian jakości powietrza**.  

---

## 🚀 Technologie  

### 🔹 Backend (Mikroserwisy)  
- **FastAPI** – szybkie i asynchroniczne API w Pythonie  
- **Google Firestore** – baza danych NoSQL w chmurze  
- **Uvicorn** – serwer ASGI dla FastAPI  
- **Pydantic** – walidacja danych wejściowych  
- **Logging** – monitorowanie działania aplikacji  

### 🔹 Frontend  
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
🔜 **Rozbudowany interfejs w React**  

---

## 🛠 Instrukcja uruchomienia backendu  

### 1️⃣ Klonowanie repozytorium  
```bash
git clone https://github.com/Roisik12/ProjektGrupowy.git
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
4️⃣ Konfiguracja Firestore & Firebase
Projekt wymaga dwóch plików kluczowych, które nie są dostępne w repozytorium:

firestore_key.json – klucz do Google Firestore
firebase_console_key.json – klucz do Firebase Authentication

🔹 Gdzie dodać pliki?
Umieść je w katalogu backend/:
```bash
ProjektGrupowy/
│── backend/
│   ├── firestore_key.json
│   ├── firebase_console_key.json
│   └── ...
```
📌 Upewnij się, że te pliki są dodane do .gitignore!


### 5️⃣ Uruchomienie mikroserwisu air-quality-service
```bash
cd backend
uvicorn air_quality_service.main:app --host 0.0.0.0 --port 8001 --reload
```
### 📌 Testowanie:
Swagger UI: http://127.0.0.1:8001/docs
Sprawdzenie jakości powietrza:
```bash
curl -X GET "http://127.0.0.1:8001/air-quality/Warsaw"
```
6️⃣ Uruchomienie mikroserwisu prediction-service
```bash
cd backend
uvicorn prediction_service.main:app --host 0.0.0.0 --port 8002 --reload
```
🔹 Testowanie:
Swagger UI: http://127.0.0.1:8002/docs

Sprawdzenie przewidywanej jakości powietrza:

```bash
curl -X GET "http://127.0.0.1:8002/predict/Warsaw"
```


🎨 Uruchomienie frontendu (React)
1️⃣ Instalacja zależności
```bash
cd frontend
npm install
```
2️⃣ Uruchomienie aplikacji
```bash
npm start
```
🔹 Aplikacja będzie dostępna pod adresem:
http://localhost:3000

🐳 Uruchomienie za pomocą Dockera
🔹 Budowanie obrazu Dockera:
```bash
docker build -t projektgrupowy .
```
🔹 Uruchamianie kontenera:

```bash
docker run -p 8001:8001 -p 8002:8002 projektgrupowy
```
🔹 Uruchamianie aplikacji React w kontenerze:
```bash
docker run -p 3000:3000 projektgrupowy-frontend
```

### 👨‍💻 Autorzy
Maciej Łapiński

Maksymilian Wyszatycki

Filip Pławiński

