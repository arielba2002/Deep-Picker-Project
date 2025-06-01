# Use Python 3.12 slim as the base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    HOST=0.0.0.0 \
    PORT=8888 \
    PYTHONPATH=/app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create matplotlib cache directory and set permissions
RUN mkdir -p /app/.config/matplotlib && \
    chmod -R 777 /app/.config

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY pyproject.toml ./

# Install dependencies directly using pip
RUN pip install --no-cache-dir \
    --no-warn-script-location \
    fastapi==0.115.6 \
    uvicorn==0.34.0 \
    sqlalchemy==2.0.37 \
    psycopg2-binary==2.9.10 \
    databases==0.9.0 \
    pydantic==2.10.5 \
    asyncpg==0.30.0 \
    tensorflow==2.19.0 \
    pandas==2.2.3 \
    matplotlib==3.10.1 \
    scikit-learn==1.6.1 \
    passlib[bcrypt]==1.7.4 \
    python-jose==3.4.0 \
    python-multipart==0.0.20 \
    bcrypt==4.3.0

# Copy the rest of the application
COPY . .

# Expose the port the app runs on
EXPOSE 8888

# Command to run the application with auto-reload for development
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8888", "--reload"]
