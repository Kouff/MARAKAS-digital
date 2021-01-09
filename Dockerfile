FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /flask

COPY . /flask
RUN pip install -r /flask/requirements.txt