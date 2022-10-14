FROM python:3.9.6-alpine

WORKDIR /tg_bot/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ADD . . /tg_bot/

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

