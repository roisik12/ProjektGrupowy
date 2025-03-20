# Use Node.js as the base image
FROM node:18

# Set the working directory inside the container
WORKDIR /app

# Copy frontend dependencies and install them
COPY frontend/package.json frontend/package-lock.json ./
RUN npm install

# Copy the frontend source code
COPY frontend/ ./

# start the frontend (React app)
RUN npm run build

# Expose the frontend port
EXPOSE 3000

# Start the frontend server
CMD ["npm", "start"]
