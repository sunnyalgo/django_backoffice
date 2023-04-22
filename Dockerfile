FROM python:3.11.2-slim

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install --no-install-recommends -y make gcc python-dev wkhtmltopdf libpq-dev && \
    apt clean && \
    apt autoclean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /opt/django_backoffice

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /opt/django_backoffice