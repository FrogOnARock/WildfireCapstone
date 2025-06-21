# Use full Python 3.11 image to avoid ML compatibility issues
FROM python:3.11

LABEL maintainer="Mackenzie Rock"

# Avoid bytecode generation and buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system-level dependencies
RUN apt-get update && \
    apt-get install -y build-essential && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy app files
COPY . .

# Expose ports for FastAPI and Streamlit
EXPOSE 8000 8501

# Start FastAPI (8000) and Streamlit (8501) concurrently
CMD ["bash", "-c", "uvicorn wildfire_1.app.main:app --host 0.0.0.0 --port 8000 & streamlit run wildfire_1/app/streamlit_app/Home.py --server.port=8501 --server.enableCORS=false"]
