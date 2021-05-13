#!/usr/bin/env python3

import logging
from time import sleep
import sys

import redis
from influxdb import InfluxDBClient

import config

SERVCE_CHECK_INTERVAL = 60  # seconds


logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
log = logging


def process_redis_server(influx_client, redis_server, redis_port, redis_namespace):
    """ 
        Fetch metrics from a given redis server and send them to the provided
        influx server.
    """

    log.info("Check %s %s", redis_server, redis_client)
    r = redis.Redis(host=redis_server, port=redis_port, namespace=namespace)



def main():
    """ Main application loop """

    log.info("metric writer starting!")
    while True:

        try:
            client = InfluxDBClient(config.INFLUX_SERVER, config.INFLUX_PORT, 'root', 'root') 
        except Exception as err:
            log.error("Cannot make connection to influx: %s", str(err))
            sleep(3)
            sys.exit(-1)

        for redis_server, redis_port, redis_namespace in config.redis_servers: 
            process_redis_server(redis_server, redis_port, redis_namespace)

        sleep(SERVCE_CHECK_INTERVAL)


if __name__ == "__main__":
    main()
