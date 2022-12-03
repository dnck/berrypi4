"""Application exporter"""

import os
from prometheus_client import start_http_server, Gauge
import time
import adafruit_dht
from board import *


def c_to_f(c):
    return (c*1.8) + 32

def read_thermometer():
    SENSOR_PIN = D4
    dht22 = adafruit_dht.DHT22(SENSOR_PIN, use_pulseio=False)
    dht22.measure()
    temp = dht22.temperature
    humi = dht22.humidity
    return humi, temp, c_to_f(temp)

def metrics():
    collected = False
    while not collected:
        try:
            humi, temp_c, temp_f = read_thermometer()
            if humi > -1:
                collected = True
        except:
            continue
    return humi, temp_c, temp_f


class AppMetrics:
    """
    Representation of Prometheus metrics and loop to fetch and transform
    application metrics into Prometheus metrics.
    """

    def __init__(self, app_port=80, polling_interval_seconds=5):
        self.app_port = app_port
        self.polling_interval_seconds = polling_interval_seconds

        # Prometheus metrics to collect
        self.humid = Gauge("rel_humid", "Relative humidity")
        self.tempc = Gauge("temp_c", "Temp in celsius")
        self.tempf = Gauge("temp_f", "Temp in fahrenheit")

    def run_metrics_loop(self):
        """Metrics fetching loop"""
        while True:
            self.fetch()
            time.sleep(self.polling_interval_seconds)

    def fetch(self):
        """
        Get metrics from application and refresh Prometheus metrics with
        new values.
        """
        # Fetch raw status data from the application
        humid, tempc, tempf = metrics()
        # Update Prometheus metrics with application metrics
        self.humid.set(humid)
        self.tempc.set(tempc)
        self.tempf.set(tempf)

def main():
    """Main entry point"""

    polling_interval_seconds = int(os.getenv("POLLING_INTERVAL_SECONDS", "10"))
    app_port = int(os.getenv("APP_PORT", "9999"))
    exporter_port = int(os.getenv("EXPORTER_PORT", "8080"))

    app_metrics = AppMetrics(
        app_port=app_port,
        polling_interval_seconds=polling_interval_seconds
    )
    start_http_server(exporter_port)
    app_metrics.run_metrics_loop()

if __name__ == "__main__":
    main()
