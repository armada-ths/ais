FROM python

ENV PYTHONUNBUFFERED 1

RUN apt-get update -y
RUN apt-get -y install binutils libproj-dev gdal-bin

RUN mkdir /ais
WORKDIR /ais/

ADD requirements.txt /ais/
RUN pip install -r requirements.txt

ADD . /ais/
