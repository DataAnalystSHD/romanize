FROM python:3.10-slim

WORKDIR /app
COPY . /app

# Upgrade pip & install dependencies, directly from GitHub zip
RUN pip install --upgrade pip
RUN pip install flask pythainlp \
    https://github.com/PyThaiNLP/thai2rom/archive/refs/heads/main.zip

EXPOSE 8080
CMD ["python", "app.py"]
