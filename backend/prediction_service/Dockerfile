# Stage 1 - build dependencies
FROM python:3.12-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first to leverage Docker cache
COPY backend/prediction_service/requirements.txt .

# Upgrade pip and install requirements
RUN pip install --upgrade pip \
 && pip install --cache-dir=/pip_cache -r requirements.txt

# Stage 2 - final app
FROM python:3.12-slim

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY backend/prediction_service /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]