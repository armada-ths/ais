FROM python:3

ENV PYTHONUNBUFFERED 1

RUN apt-get update -y
RUN apt-get -y install binutils libproj-dev gdal-bin npm nodejs

RUN mkdir /ais
WORKDIR /ais/

RUN npm install
ADD requirements.txt /ais/
RUN pip install -r requirements.txt

ADD . /ais/
