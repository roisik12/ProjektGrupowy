# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Install required packages: curl, gnupg2, supervisor, and other dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gnupg2 \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js (LTS version, e.g., Node 16)
RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy entire project into the container
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Install Node dependencies for the frontend
WORKDIR /app/frontend
RUN npm install

# Expose ports used by the services (8001, 8002, 3000)
EXPOSE 8001 8002 3000

# Copy Supervisor configuration into the container
WORKDIR /app
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Run Supervisor to start all services
CMD ["supervisord", "-n"]
