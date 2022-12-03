#!/bin/bash
sudo cp home-metrics.service /etc/systemd/system/home-metrics.service
sudo /bin/systemctl daemon-reload
sudo /bin/systemctl enable home-metrics.service
sudo /bin/systemctl start home-metrics.service
