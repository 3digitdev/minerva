#!/usr/bin/env bash

# Setup Mongo configuration
sudo tee /etc/mongod.conf > /dev/null << EOT
storage:
    dbPath: /var/lib/mongodb
    journal:
        enabled: true

systemLog:
    destination: file
    logAppend: true
    path: /var/log/mongodb/mongod.log
    logRotate: reopen

net:
    port: 27017
    bindIp: 127.0.0.1

processManagement:
    pidFilePath: /var/run/mongodb/mongod.pid
    timeZoneInfo: /usr/share/zoneinfo
EOT

# Setup collections and indices
mongo initMongo.js