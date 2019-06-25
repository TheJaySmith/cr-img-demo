FROM python:3.7-stretch

MAINTAINER Jay Smith "jaysmith@google.com"

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

COPY ./requirements.txt /app/requirements.txt

ENV APP_HOME /app

ENV UPLOAD_DIR /app/upload

WORKDIR $APP_HOME

RUN pip install -r requirements.txt

COPY . /app

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app
