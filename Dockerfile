# Use a lightweight python base image
FROM python:3.11-slim

# Set environment variables to keep Python clean and responsive
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy dependency specifications first to leverage Docker layer caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code and vendored libraries
COPY google/ ./google/
COPY tools.py .
COPY social_agent.py .
COPY main.py .
COPY static/ ./static/

# Expose standard port 8080 (Cloud Run listens on 8080 by default, but it can vary)
EXPOSE 8080

# Run FastAPI app with Uvicorn, dynamically binding to the $PORT env var set by Cloud Run
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}"]
