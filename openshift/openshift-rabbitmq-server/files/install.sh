#!/bin/sh
mkdir -p /var/log/comodit/rabbitmq-server

(
# Enable Stom plugin
export HOME=/root/
/usr/lib/rabbitmq/bin/rabbitmq-plugins enable rabbitmq_stomp
/bin/systemctl restart rabbitmq-server.service

) > /var/log/comodit/rabbitmq-server/install.log 2>&1
