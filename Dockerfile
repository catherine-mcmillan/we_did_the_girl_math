FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create data directory and set permissions
RUN mkdir -p /app/data && \
    if [ -f app.db ]; then mv app.db /app/data/; else touch /app/data/app.db; fi && \
    chmod 777 /app/data/app.db

# Create non-root user
RUN useradd -m appuser && \
    chown -R appuser:appuser /app

USER appuser

# Expose the port
ENV PORT=8080
EXPOSE 8080

# Initialize database and start the application
CMD ["sh", "-c", "python init_db.py && gunicorn --bind 0.0.0.0:${PORT:-8080} \"run:app\""]