# Use Python 3.12 slim as the base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    HOST=0.0.0.0 \
    PORT=8888 \
    PYTHONPATH=/app \
    MPLCONFIGDIR=/tmp/matplotlib

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    netcat-openbsd \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create matplotlib cache directory and set permissions
RUN mkdir -p /tmp/matplotlib && \
    chmod -R 777 /tmp/matplotlib

# Set working directory
WORKDIR /app

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies in a single layer
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create a startup script
RUN echo '#!/bin/sh\n\
echo "Starting backend service..."\n\
echo "Testing database connection..."\n\
nc -zv db 5432\n\
if [ $? -eq 0 ]; then\n\
    echo "Database connection successful"\n\
else\n\
    echo "Database connection failed"\n\
    exit 1\n\
fi\n\
echo "Starting uvicorn server..."\n\
echo "Testing if port 8888 is available..."\n\
nc -zv localhost 8888\n\
if [ $? -eq 0 ]; then\n\
    echo "Port 8888 is already in use"\n\
    exit 1\n\
else\n\
    echo "Port 8888 is available"\n\
fi\n\
echo "Starting uvicorn server on port 8888..."\n\
exec uvicorn main:app --host 0.0.0.0 --port 8888 --log-level debug\n\
' > /app/start.sh && chmod +x /app/start.sh

# Expose the port the app runs on
EXPOSE 8888

# Use the startup script
CMD ["/app/start.sh"]
