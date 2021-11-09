# syntax=docker/dockerfile:1
FROM python:3

ENV PYTHONUNBUFFERED 1

RUN apt-get update -y \
    && apt-get install -y --no-install-recommends \
    binutils=2.35.2-2 \
    libproj-dev=7.2.1-1 \
    gdal-bin=3.2.2+dfsg-2 \
    npm=7.5.2+ds-2 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /vagrant
WORKDIR /vagrant/

RUN npm install

RUN python -m pip install --upgrade pip
RUN python -m venv ais_venv
RUN . ais_venv/bin/activate

COPY requirements.txt /vagrant/
RUN ./ais_venv/bin/pip install -r requirements.txt

COPY . /vagrant/

RUN npm run build
