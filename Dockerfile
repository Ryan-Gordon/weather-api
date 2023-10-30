# Use an official Python runtime as the base image
FROM python:3.10-slim

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Define environment variable for the SQLite database
ENV SQLLITE_DB_LOCATION sqlite:///weather.db
ENV WEATHER_API_PORT 8080

# Use python app.py as the entrypoint
CMD ["python", "app.py"]

# Make port 8080 available for the app
EXPOSE 8080
