# Use Python as the base image
FROM python:3.12

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY backend/air_quality_service/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the air quality service files into the container
COPY backend/air_quality_service/ ./air_quality_service/

# Expose the API port
EXPOSE 8001

# Set the default command to start the FastAPI service
CMD ["uvicorn", "air_quality_service.main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
