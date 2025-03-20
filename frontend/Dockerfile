# Use Node.js as the base image
FROM node:18

# Set the working directory inside the container
WORKDIR /app

# Copy package.json (ignore package-lock.json if missing)
COPY frontend/package.json ./

# Ensure package-lock.json exists (if missing, create an empty one)
RUN [ -f package-lock.json ] || echo '{}' > package-lock.json

# Install dependencies
RUN npm install

# Copy the entire frontend source code AFTER dependencies are installed
COPY frontend/ ./

# Build the React app (production-ready)
RUN npm run build

# Expose the frontend port
EXPOSE 3000

# Set the default command to start the React development server
CMD ["npm", "start"]
