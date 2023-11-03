# Use the official Python image from Docker Hub as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy your application code into the container
COPY . /app

# Copy the requirements.txt file into the working directory
COPY requirements.txt .

# Install any required dependencies and clean up to reduce image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy the 'service' package into the working directory with the same name
COPY service/ ./service/

# Create a non-root user 'theia' and set the ownership of /app to 'theia'
Run useradd --uid 1000 theia && chown -R theia /app
USER theia

# Expose port 8080 for incoming connections
EXPOSE 8080

# Specify the command to run when the container starts
CMD ["gunicorn", "--bind=0.0.0.0:8080", "--log-level=info", "service:app"]

ENV DATABASE_URI=postgresql://postgres:pgs3cr3t@postgres:5432/testdb