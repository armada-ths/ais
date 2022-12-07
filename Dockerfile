# Pull offical base image
FROM python:3.10.1-alpine

# Set work directory
WORKDIR /usr/src/app

# SET ENVIRONMENT VARIABLES
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies
RUN apk update \
  && apk add --no-cache gcc python3-dev musl-dev libffi-dev \
  gdal-dev linux-headers g++ binutils geos-dev

# Prerequsite for Pillow
RUN apk add tiff-dev jpeg-dev openjpeg-dev zlib-dev freetype-dev lcms2-dev \
    libwebp-dev tcl-dev tk-dev harfbuzz-dev fribidi-dev libimagequant-dev \
    libxcb-dev libpng-dev

# Install dependencies
RUN pip install --upgrade pip==21.3.1
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# COPY 'entrypoint.sh'
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# Copy project
COPY . .

# Node
RUN apk add npm
RUN npm install
RUN npm run build

### 

# RUN 'entrypoint.sh'
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

EXPOSE 8080
EXPOSE 3000

