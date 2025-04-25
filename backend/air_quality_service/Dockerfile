# Stage 1 - build dependencies
FROM python:3.12-slim AS builder

WORKDIR /app

# Kopiujemy tylko requirements, żeby cache nie przepadał
COPY backend/air_quality_service/requirements.txt .

RUN pip install --upgrade pip \
 && pip install --cache-dir=/pip_cache -r requirements.txt

# Stage 2 - final app
FROM python:3.12-slim

WORKDIR /app

# Skopiuj zależności
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# 🧠 To jest ważne! Skopiuj cały katalog backend, nie tylko `air_quality_service`
COPY backend /app/backend

# Dodaj plik main.py do /app jeśli jest wyżej
COPY backend/air_quality_service/main.py /app/main.py

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]