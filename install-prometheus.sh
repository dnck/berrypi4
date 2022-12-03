#!/bin/bash
wget https://github.com/prometheus/prometheus/releases/download/v2.34.0/prometheus-2.34.0.linux-armv7.tar.gz
tar xfz prometheus-2.34.0.linux-armv7.tar.gz
mv prometheus-2.34.0.linux-armv7.tar.gz prometheus
mkdir prometheus/data
mv prometheus.yml ./prometheus/
cp prometheus.service /etc/systemd/system/prometheus.service
