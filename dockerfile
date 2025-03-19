# Stage 1: Build Frontend
FROM node:18 AS frontend-build
WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm install
COPY frontend ./
RUN npm run build

# Stage 2: Backend (Python)
FROM python:3.12 AS backend
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend and frontend build
COPY backend /app/backend
COPY supervisord.conf /app/supervisord.conf
COPY --from=frontend-build /app/frontend/build /app/frontend/build

# Expose ports
EXPOSE 8001 8002 3000

# Start everything with Supervisor
CMD ["/usr/bin/supervisord", "-c", "/app/supervisord.conf"]
