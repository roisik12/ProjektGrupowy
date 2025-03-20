# Use Python as the base image
FROM python:3.12

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY backend/prediction_service/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the prediction service files into the container
COPY backend/prediction_service/ ./prediction_service/

# Expose the API port
EXPOSE 8002

# Set the default command to start the FastAPI service
CMD ["uvicorn", "prediction_service.main:app", "--host", "0.0.0.0", "--port", "8002", "--reload"]
