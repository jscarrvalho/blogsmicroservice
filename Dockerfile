FROM python:3.11
ENV PYTHONUNBUFFERED=1

RUN apt-get update -y && DEBIAN_FRONTEND=noninteractive apt-get install -y gcc libc-dev default-libmysqlclient-dev gettext xmlsec1

WORKDIR /blogsmicroservice

# Install dependencies
COPY blogsmicroservice/requirements.txt .
RUN pip install -r requirements.txt

COPY .. .
