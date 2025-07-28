# Simplified Dockerfile for Adobe Hackathon Solution - Round 1A Only

FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies only (no system dependencies needed)
RUN pip install --no-cache-dir -r requirements.txt

# Copy solution code
COPY solution/ ./solution/

# Create input and output directories
RUN mkdir -p /app/input /app/output

# Set the entry point
ENTRYPOINT ["python", "solution/main.py"] 