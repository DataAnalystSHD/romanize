FROM python:3.10-slim

WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install -y gcc g++ libffi-dev git

RUN pip install --upgrade pip
RUN pip install flask \
    https://github.com/PyThaiNLP/pythainlp/archive/dev.zip

EXPOSE 8080
CMD ["python", "app.py"]
