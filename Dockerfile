# SHADOW-BRIDGE DOCKERFILE v1.0
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python requirements
# Note: In a full commercial repo, we'd use requirements.txt
RUN pip install --no-cache-dir fastapi uvicorn pydantic==2.0.0 oandapyV20 requests

# Copy source code
COPY . .

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Expose FastAPI port
EXPOSE 8000

# Level 5 Sovereignty: Run as non-privileged user
RUN useradd -m trishula
USER trishula

# Launch the Bridge
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
