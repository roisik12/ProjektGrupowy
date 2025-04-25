# Stage 1 - build dependencies
FROM python:3.12-slim AS builder

WORKDIR /app

# Copy only requirements first
COPY backend/air_quality_service/requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Stage 2 - final app
FROM python:3.12-slim

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

# Copy application code
COPY backend /app/backend
COPY backend/air_quality_service/main.py /app/main.py

# Set Python path to include backend directory
ENV PYTHONPATH=/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
