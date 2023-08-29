FROM python:3.10.1-alpine as base
WORKDIR /usr/src/app

FROM base as frontend-dashboard
RUN apk add npm
RUN npm add pnpm -g

COPY ./apps/complete_registration/package.json ./apps/complete_registration/pnpm-lock.yaml ./apps/complete_registration/
RUN cd ./apps/complete_registration && pnpm install

COPY ./apps/complete_registration ./apps/complete_registration
RUN cd ./apps/complete_registration && pnpm build

COPY ./apps/complete_registration/output.css ./apps/complete_registration/dist/index.css

FROM base as frontend
RUN apk add npm

COPY package.json package-lock.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM base as backend

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
  && apk add --no-cache gcc python3-dev musl-dev libffi-dev \
  gdal-dev linux-headers g++ binutils geos-dev \
  tiff-dev jpeg-dev openjpeg-dev zlib-dev freetype-dev lcms2-dev \
  libwebp-dev tcl-dev tk-dev harfbuzz-dev fribidi-dev libimagequant-dev \
  libxcb-dev libpng-dev

RUN pip install --upgrade pip==21.3.1
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

COPY --from=frontend /usr/src/app/webpack-stats.js ./
COPY --from=frontend /usr/src/app/ais_static/bundles ./ais_static/bundles
COPY --from=frontend-dashboard /usr/src/app/apps/complete_registration/dist ./ais_static/apps/complete_registration

RUN SECRET_KEY=123 python manage.py collectstatic --noinput

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

EXPOSE 3000

