FROM ubuntu:16.04
MAINTAINER Vidispine AB

RUN apt-get update -y && apt-get install -y --no-install-recommends \
    curl \
    nginx \
    python3.5 \
    python-software-properties \
    software-properties-common \
    supervisor \
    vim \
 && curl -sL https://deb.nodesource.com/setup_8.x | bash \
 && apt-get update -y && apt-get install -y --no-install-recommends \
    nodejs \
 && rm -rf /var/lib/apt/lists/*

RUN echo "error_log /dev/stderr info;\ndaemon off;" >> /etc/nginx/nginx.conf \
 && sed -i 's/# gzip_/gzip_/g' /etc/nginx/nginx.conf

# Docker specific configuration
COPY packaging/entrypoint.sh /
COPY packaging/poi.config.js /opt/vidispine-content-viewer/

# Packages
COPY requirements.pip /opt/vidispine-content-viewer/
COPY package.json /opt/vidispine-content-viewer/
COPY yarn.lock /opt/vidispine-content-viewer/
COPY packaging/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY packaging/uwsgi.ini /opt/vidispine-content-viewer/

# Application
COPY index.html /opt/vidispine-content-viewer/
COPY manage.py /opt/vidispine-content-viewer/
COPY .eslintrc.js /opt/vidispine-content-viewer/
COPY src/ /opt/vidispine-content-viewer/src/
COPY static/ /opt/vidispine-content-viewer/static/
COPY app/ /opt/vidispine-content-viewer/app/

# Application components
COPY vdt_python_sdk-0.9.tar.gz /opt/vidispine-content-viewer/
COPY vdt-vue-components/ /opt/vidispine-content-viewer/vdt-vue-components/

WORKDIR /opt/vidispine-content-viewer/

RUN buildDeps='gcc git zlib1g-dev libxml2-dev libxml2-utils libxslt1-dev python3-pip python3-dev python3-setuptools'; \
    set -x \
 && apt-get update && apt-get install -y --no-install-recommends $buildDeps \
 && rm -rf /var/lib/apt/lists/* \
 && npm install -g yarn \
 && python3 -m pip install --upgrade pip wheel \
 && python3 -m pip install --no-cache-dir -r /opt/vidispine-content-viewer/requirements.pip \
 && node --version \
 && python3 -m pip install uwsgi \
 && python3 -m pip install --upgrade /opt/vidispine-content-viewer/vdt_python_sdk-0.9.tar.gz \
 && yarn install --pure-lockfile --production=false --non-interactive \
 && (cd vdt-vue-components && yarn install --pure-lockfile --production=false --non-interactive && yarn build && yarn link) \
 && yarn link @vidispine/vdt-vue-components \
 && mkdir app/dist \
 && yarn build \
 && python3 ./manage.py collectstatic \
 && cp dist/* app/collected_static \
 && rm -rf ./node_modules/ ./vdt-vue-components/node_modules/ ./app/dist/ /root/.cache/ /usr/local/share/.cache/ \
 && apt-get purge -y --auto-remove $buildDeps


COPY packaging/nginx.conf /etc/nginx/sites-enabled/default

ENV VIDISPINE_IP_PORT='vidispine:8080'
ENV HTTPS='true'

EXPOSE 80
ENTRYPOINT ["/entrypoint.sh"]
CMD ["server"]
