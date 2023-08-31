FROM python:3.10.1-alpine as base
RUN apk update

FROM base as frontend-base
RUN apk add npm

FROM frontend-base as frontend-dashboard
WORKDIR /usr/src/dashboard
RUN npm add pnpm -g

COPY ./apps/complete_registration/package.json ./apps/complete_registration/pnpm-lock.yaml .
RUN pnpm install

COPY ./apps/complete_registration .
RUN pnpm build

FROM frontend-base as frontend
WORKDIR /usr/src/app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM base as backend
WORKDIR /usr/src/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk add --no-cache gcc python3-dev musl-dev libffi-dev \
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

RUN ./create_static_apps_directory.sh
COPY --from=frontend-dashboard /usr/src/dashboard/dist ./ais_static/apps/complete_registration

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

EXPOSE 3000

