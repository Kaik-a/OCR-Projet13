#!/bin/bash
USER=$1
PASSWORD=$2
SAVE_DIRECTORY=$3

echo "*:*:*:*:$PASSWORD" > ~/.pgpass

chmod 0600 ~/.pgpass

echo "Create hour-to-hour backup job"
(crontab -l ; echo "00 * * * * /etc/gamelenders/backup.sh $USER $SAVE_DIRECTORY >> /etc/gamelenders/logs/backup.log 2>&1") | crontab
