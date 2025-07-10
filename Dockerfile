FROM python:3.10-slim

WORKDIR /app
COPY . /app

# Install git so we can pip install from git+ URLs
RUN apt-get update && apt-get install -y git

# Upgrade pip & install everything
RUN pip install --upgrade pip
RUN pip install flask pythainlp git+https://github.com/PyThaiNLP/thai2rom.git

EXPOSE 8080
CMD ["python", "app.py"]
