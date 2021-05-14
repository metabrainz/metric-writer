#!/usr/bin/env python3

import logging
from time import sleep
import sys

import redis
from influxdb import InfluxDBClient

from brainzutils.metrics import REDIS_METRICS_KEY
import config

SERVCE_CHECK_INTERVAL = 60  # seconds


logging.basicConfig(encoding='utf-8', level=logging.INFO)
log = logging


def process_redis_server(client, redis_server, redis_port, redis_namespace):
    """ 
        Fetch metrics from a given redis server and send them to the provided
        influx server. If a metric cannot be submitted, log and error and discard
        the metric and carry on.
    """

    r = redis.Redis(host=redis_server, port=redis_port)

    points = []
    while True:
        line = r.lpop(REDIS_METRICS_KEY)
        if not line:
            break

        line = str(line, "utf-8")
        points.append(line)

    try:
        client.write_points(points, protocol="line")
    except Exception as err:
        self.log.error("Cannot write metric to influx: %s" % str(err))



def main():
    """ Main application loop """

    log.info("metric writer starting!")
    while True:

        try:
            client = InfluxDBClient(config.INFLUX_SERVER, config.INFLUX_PORT, 'root', 'root', "service-metrics") 
        except Exception as err:
            log.error("Cannot make connection to influx: %s", str(err))
            sleep(3)
            sys.exit(-1)

        for info in config.redis_servers: 
            process_redis_server(client, info["host"], info["port"], info["namespace"])

        sleep(SERVCE_CHECK_INTERVAL)

    write_api.close()
    client.close()


if __name__ == "__main__":
    main()
