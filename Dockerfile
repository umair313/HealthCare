FROM python:3.9-bookworm

ENV PYTHONUNBUFFERED 1

RUN apt update

RUN mkdir /code
WORKDIR /code

COPY requirements.prod.txt /code/requirements.txt

RUN pip install --upgrade pip
RUN pip install -r /code/requirements.txt