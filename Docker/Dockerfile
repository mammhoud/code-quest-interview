FROM python:3.11-alpine
# Set environment variables
# ARG PYTHON_VERSION=3.11

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND noninteractive

# # download and extract python sources
# RUN cd /opt \
#     && wget https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz \
#     && tar xzf Python-${PYTHON_VERSION}.tgz

# # build python and remove left-over sources
# RUN cd /opt/Python-${PYTHON_VERSION} \
#     && ./configure --prefix=/usr --enable-optimizations --with-ensurepip=install \
#     && make install \
#     && rm /opt/Python-${PYTHON_VERSION}.tgz /opt/Python-${PYTHON_VERSION} -rf


RUN apk add --virtual .build-deps gcc musl-dev wget \
    gcc \
    make \
    zlib-dev \
    libffi-dev \
    openssl-dev \
    musl-dev && \
    apk add nginx \
    pipx

    # apk add --update --no-cache python3 && \
    # ln -sf python3 /usr/bin/python && \
    # python -m pip3 install --no-cache --upgrade pip setuptools


ADD ./ /app/
WORKDIR /app

# Installing all python dependencies
# RUN pip install -r requirements.txt
# && \    apk del .build-deps

# RUN pip install --no-cache-dir -r requirements/dev.txt

COPY docker/nginx/nginx.conf /etc/nginx/nginx.conf
COPY docker/nginx/default.conf /etc/nginx/conf.d/default.conf
# COPY docker/scripts /scripts

RUN chmod +x docker/scripts/webserver-start.sh
RUN chmod +x docker/scripts/worker-start.sh
RUN chmod +x docker/scripts/beat-start.sh

RUN pipx install hatch;
RUN python -m pip install --no-cache --upgrade pip setuptools;
RUN python -m pip install hatch;
# RUN hatch env show
# Use file.name* in case it doesn't exist in the repo
# RUN hatch env prune
# RUN hatch env create production && pip install --upgrade setuptools
# ENTRYPOINT ["/app/docker/scripts/webserver-start.sh"] # at docker volume
