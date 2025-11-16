# Use an official Python runtime as a parent image
FROM python:3.9-slim

WORKDIR /app

# Install Flask
RUN pip install Flask

# Copy the server script
COPY rest_server.py .

# Expose the Flask port
EXPOSE 5000

# Run the server
CMD ["python", "rest_server.py"]