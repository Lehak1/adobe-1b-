# Use slim Python base image
FROM python:3.10-slim

# Install basic system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    poppler-utils \
    libglib2.0-0 \
    && apt-get clean

# Set working directory
WORKDIR /app

# Copy requirements first for layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# NLTK tokenizer data
RUN python -c "import nltk; nltk.download('punkt')"

# Copy the app code
COPY . .

# Default command
CMD ["python", "main.py", "sample_input.json", "output.json"]
