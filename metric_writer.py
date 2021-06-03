#!/usr/bin/env python3

import logging
from time import sleep, monotonic
import sys

import redis
import sentry_sdk
import requests

from brainzutils.metrics import REDIS_METRICS_KEY
import config

SERVCE_CHECK_INTERVAL = 15  # seconds
REPORT_INTERVAL = SERVCE_CHECK_INTERVAL * 40


logging.basicConfig(encoding='utf-8', level=logging.INFO)
log = logging


def process_redis_server(redis_server, redis_port, redis_namespace):
    """ 
        Fetch metrics from a given redis server and send them to the provided
        influx server. If a metric cannot be submitted, log the error, sleep
        for a few seconds and retry. The data point is never discarded. We
        only exit on a successful or client error response.
    """

    r = redis.Redis(host=redis_server, port=redis_port)

    lines = ""
    count = 0
    while True:
        line = r.lpop(REDIS_METRICS_KEY)
        if not line:
            break

        lines += str(line, "utf-8")
        count += 1

    if not lines:
        return 0

    params = {"p": "root", "db": "service-metrics", "u": "root"}
    timeout_notification = monotonic() + 3600
    while True:
        try:
            r = requests.post("http://%s:%d/write" % (config.INFLUX_SERVER,
                                                      config.INFLUX_PORT), params=params, data=lines)
            if r.status_code in (200, 204):
                return count
            elif str(r.status_code)[0] == '4':
                log.error("Cannot write metric due to 4xx error. %s" % r.text)
                return 0
            else:
                error = r.text
        except Exception as error:
            pass
        log.warning(
            "Cannot write metric due to other error Retyring. %s" % error)
        if monotonic() > timeout_notification:
            timeout_notification += 3600
            log.error(
                "Unable to submit metrics for quite some time. Something is surely broken! Error: %s" % error)

        sleep(30)


def main():
    """ Main application loop """

    # attempt to initialize sentry_sdk only if configuration available
    if hasattr(config, 'LOG_SENTRY'):
        sentry_sdk.init(**config.LOG_SENTRY)

    log.info("metric writer starting!")
    count = 0
    update_time = monotonic() + REPORT_INTERVAL
    while True:
        for info in config.redis_servers:
            count += process_redis_server(info["host"],
                                          info["port"], info["namespace"])

        sleep(SERVCE_CHECK_INTERVAL)
        if monotonic() > update_time:
            update_time += REPORT_INTERVAL
            log.info("Submitted %s data points" % count)


if __name__ == "__main__":
    main()
