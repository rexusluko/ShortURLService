FROM python:3.8

ENV PYTHONUNBUFFERED 1

WORKDIR /shorturl

COPY requirements.txt /shorturl/
RUN pip install -r requirements.txt

COPY . /shorturl/
