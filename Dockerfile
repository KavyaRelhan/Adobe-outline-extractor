# Base image with Python
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Copy all files into container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir pymupdf

# Create input and output folders (in case they don't exist)
RUN mkdir -p input output

# Set default command
CMD ["python", "src/extract_outline.py"]