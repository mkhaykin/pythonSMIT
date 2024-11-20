FROM python:3.12-slim

#
LABEL maintainer="mkhaikin@yandex.ru"

#
RUN apt-get update  \
    && apt-get -y install

#
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /tmp/requirements.txt

#
WORKDIR .

#
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

#
COPY src /src
