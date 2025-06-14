FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir python-multipart
# Copy the rest of the application
COPY . .

# Create a non-root user
RUN useradd -m -u 1001 appuser && \
    mkdir -p /tmp/matplotlib && \
    chown -R appuser:appuser /app /tmp/matplotlib && \
    chmod 755 /tmp/matplotlib

# Switch to non-root user (OpenShift will override this with the correct user ID)
USER 1001

# Expose the port
EXPOSE 8888

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV MPLCONFIGDIR=/tmp/matplotlib

# Run the application
CMD ["python", "main.py"] 