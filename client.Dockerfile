# Use an official Python runtime as a parent image
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
RUN pip install grpcio grpcio-tools requests

# Copy the .proto file and generated code
COPY services.proto .
COPY services_pb2.py .
COPY services_pb2_grpc.py .

# Copy the client script
COPY client.py .

# Run the client
CMD ["python", "client.py"]