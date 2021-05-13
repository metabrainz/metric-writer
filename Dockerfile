ARG PYTHON_BASE_IMAGE_VERSION=3.7-20210115
FROM metabrainz/python:$PYTHON_BASE_IMAGE_VERSION as listenbrainz-base

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
                       git \
                       redis-tools \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /code/metrics

WORKDIR /code/metrics
RUN pip3 install pip==21.0.1
COPY requirements.txt /code/metrics/
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /code/metrics

COPY consul-template-config.conf /etc
COPY metric_writer.service /etc/service/metric_writer/run
