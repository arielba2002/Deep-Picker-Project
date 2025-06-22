# Use Python 3.12 slim as the base image
FROM python:3.12-slim

WORKDIR /app

# Set env vars to keep TF quiet and force CPU
ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    TF_CPP_MIN_LOG_LEVEL=2 \
    TF_ENABLE_ONEDNN_OPTS=0 \
    TF_DISABLE_SEGMENT_REDUCTION_OP=1 \
    CUDA_VISIBLE_DEVICES="" \
    TF_FORCE_GPU_ALLOW_GROWTH=false \
    NUMPY_EXPERIMENTAL_ARRAY_FUNCTION=0

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY pyproject.toml ./

# Install dependencies directly using pip
RUN pip install --no-cache-dir \
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
    bcrypt==4.3.0 \
    requests==2.32.0 \
    numpy==1.26.4 \
    scipy==1.13.0 \
    scikit-image==0.21.0
# Copy the rest of the application
COPY . .

EXPOSE 8888

# Use shell form to allow environment variable substitution
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8888}
