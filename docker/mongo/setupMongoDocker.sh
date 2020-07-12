#!/usr/bin/env bash

# Setup Mongo service (systemd)
sudo tee /lib/systemd/system/mongodb.service > /dev/null << EOT
[Unit]
Description=MongoDB Database Service
Wants=network.target
After=network.target

[Service]
Type=forking
PIDFile=/var/run/mongodb/mongod.pid
ExecStart=/usr/local/bin/mongod --config /etc/mongod.conf
ExecReload=/bin/kill -HUP $MAINPID
Restart=always
User=mongodb
Group=mongodb
StandardOutput=syslog
StandardError=syslog

[Install]
WantedBy=multi-user.target
EOT
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
# Setup Mongo Logs (logrotate)
sudo tee /etc/logrotate.d/mongod.conf > /dev/null << EOT
/var/log/mongodb/mongod.log {
    daily
    rotate 10
    size 100M
    missingok
    compress
    delaycompress
    notifempty
    create 640 mongod mongod
}
EOT
# Configure journald so it doesn't mess things up
sudo tee /etc/systemd/journald.conf > /dev/null << EOT
[Journal]
Storage=auto
Compress=yes
SystemMaxUse=100M
RuntimeMaxUse=100M
RuntimeMaxFileSize=10M
MaxRetentionSec=604800
EOT

# Start mongo service
systemctl start mongod