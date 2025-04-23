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

### 🔹 Chmura i Hosting
- **Google Cloud Platform (GCP)**
  - **Cloud Firestore** – przechowywanie danych
  - **Google Kubernetes Engine (GKE)** – orkiestracja kontenerów
  - **Google Container Registry (GCR)** – przechowywanie obrazów Dockerowych
  - **Cloud Load Balancer & Ingress** – dostęp zewnętrzny

---

## ⚙️ Funkcjonalności

✅ Sprawdzanie aktualnej jakości powietrza  
✅ Dodawanie i przechowywanie danych w Firestore  
✅ Usuwanie danych o jakości powietrza  
✅ Walidacja danych (AQI: 0-500)  
✅ Logowanie API dla lepszej kontroli błędów  
🔜 Prognozowanie jakości powietrza (AI)  
🔜 Integracja z zewnętrznymi API  
🔜 Rozbudowany interfejs w React

---

## 🛠 Instrukcja uruchomienia

### 1️⃣ Klonowanie repozytorium

```bash
git clone https://github.com/Roisik12/ProjektGrupowy.git
cd ProjektGrupowy
```

### 2️⃣ Konfiguracja kluczy Firebase/Firestore

Umieść pliki `firestore_key.json` i `firebase_console_key.json` w katalogu `backend/`.  
**Nie commituj tych plików!** Są dodane do `.gitignore`.

```
ProjektGrupowy/
│── backend/
│   ├── firestore_key.json
│   ├── firebase_console_key.json
│   └── ...
```

---

## 🔧 Uruchamianie lokalnie

### Backend (FastAPI)

1. Utwórz środowisko wirtualne i zainstaluj zależności:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

2. Uruchom mikroserwis:
    ```bash
    cd backend
    uvicorn air_quality_service.main:app --host 0.0.0.0 --port 8001 --reload
    ```

3. Testowanie:
    - Swagger UI: http://127.0.0.1:8001/docs
    - Przykład:  
      `curl -X GET "http://127.0.0.1:8001/air-quality/Warsaw"`

### Frontend (React)

1. Instalacja zależności:
    ```bash
    cd frontend
    npm install
    ```

2. Uruchomienie aplikacji:
    ```bash
    npm start
    ```
    - Aplikacja dostępna pod: http://localhost:3000

---

## 🐳 Uruchamianie przez Docker Compose (lokalnie)

```bash
docker-compose up --build
```
- Backend: http://localhost:8001  
- Frontend: http://localhost:3000

---

## ☁️ Deployment na Google Cloud (GKE)

### 1. Budowanie i pushowanie obrazów do GCR

```bash
docker build -t gcr.io/<TWÓJ_PROJECT_ID>/air-quality-service:v1 -f backend/air_quality_service/Dockerfile .
docker build -t gcr.io/<TWÓJ_PROJECT_ID>/frontend:v1 -f frontend/Dockerfile .
docker push gcr.io/<TWÓJ_PROJECT_ID>/air-quality-service:v1
docker push gcr.io/<TWÓJ_PROJECT_ID>/frontend:v1
```

### 2. Zastosowanie manifestów Kubernetes

```bash
kubectl apply -f kubernetes/01-deployment.yaml
kubectl apply -f kubernetes/02-service.yaml
kubectl apply -f kubernetes/03-hpa.yaml
kubectl apply -f kubernetes/04-ingress.yaml
```

### 3. Sprawdzanie statusu

```bash
kubectl get pods
kubectl get services
kubectl get ingress
```

### 4. Dostęp do aplikacji

- Frontend: adres IP z `kubectl get services` lub z Ingress
- Backend API: `/api/air-quality` przez Ingress

---

## 🧪 Testowanie

- Testy backendu:  
  ```bash
  pytest tests/
  ```

---

## 📄 Autorzy

- Maciej Łapiński
- Maksymilian Wyszatycki

---

**Uwaga:**  
Pamiętaj o odpowiedniej konfiguracji zmiennych środowiskowych i kluczy w środowisku produkcyjnym (np. przez Kubernetes Secrets).

