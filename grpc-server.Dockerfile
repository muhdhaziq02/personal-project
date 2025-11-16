# Use an official Python runtime as a parent image
FROM python:3.9-slim

WORKDIR /app

# Install gRPC and tools
RUN pip install grpcio grpcio-tools

# Copy the .proto file and generated code
COPY services.proto .
COPY services_pb2.py .
COPY services_pb2_grpc.py .

# Copy the server script
COPY grpc_server.py .

# Expose the gRPC port
EXPOSE 50051

# Run the server
CMD ["python", "grpc_server.py"]