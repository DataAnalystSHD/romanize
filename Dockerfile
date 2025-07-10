# Use an official Python slim image
FROM python:3.10-slim

# Set workdir
WORKDIR /app

# Copy your app files
COPY . /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install flask pythainlp git+https://github.com/PyThaiNLP/thai2rom.git

# Expose port 8080 (Render default)
EXPOSE 8080

# Run your app
CMD ["python", "app.py"]
