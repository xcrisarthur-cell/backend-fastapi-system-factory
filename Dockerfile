# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip setuptools wheel && \
    pip install psycopg2-binary && \
    pip install -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8080

# Create startup script
RUN echo '#!/bin/sh\nset -e\necho "=== Starting Backend FastAPI System Factory ==="\necho "Checking DATABASE_URL..."\nif [ -z "$DATABASE_URL" ]; then\n  echo "ERROR: DATABASE_URL is not set!"\n  exit 1\nfi\necho "DATABASE_URL is set"\necho "Running database migrations..."\nif alembic upgrade head; then\n  echo "Migrations completed successfully"\nelse\n  echo "WARNING: Migration failed, but continuing..."\nfi\necho "Starting server on port 8080..."\nexec uvicorn app.main:app --host 0.0.0.0 --port 8080' > /app/start.sh && chmod +x /app/start.sh

# Run startup script
CMD ["/app/start.sh"]

