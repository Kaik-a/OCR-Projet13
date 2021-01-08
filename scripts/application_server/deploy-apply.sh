#!/bin/bash
SQL_PASSWORD=$1
HOST=$2
USER=$3
CLIENT_SECRET_KEY="secret_key_we_gave_to_client"

echo "Installing python"
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python3.8
sudo apt-get install python3-venv

echo "Initializing venv"
python3.8 -m venv /etc/gamelenders/venv

echo "Activate venv"
source /etc/gamelenders/bin/activate

echo "Installing requirements"
pip install -r /etc/gamelenders/requirements.txt

echo "Installing supervisor"
sudo apt-get install supervisor

echo "Writing supervisor conf file"
echo "[program:gamelenders-gunicorn]
command = /etc/gamelenders/venv/bin/newrelic-admin run-program /etc/gamelenders/venv/bin/gunicorn -b 0.0.0.0:8000 gamelenders.wsgi
user = $USER
directory = /etc/gamelenders/
autostart = true
autorestart = true
environment = P13_SQL_PASSWORD=\"$SQL_PASSWORD\",P13_SECRET_KEY=\"$CLIENT_SECRET_KEY\",DJANGO_SETTINGS_MODULE='settings.production',HOST=$HOST, PATH=$PATH:/etc/gamelenders/venv,GIANTBOMB='a34ab727e9782db7cd136611c93065d3480aed66'
stderr_events_enabled = true
redirect_stderr = true
stdout_logfile = /etc/gamelenders/logs/gunicorn.log
stderr_logfile = /etc/gamelenders/logs/gunicorn_err.log" > /etc/supervisor/conf.d/gamelenders-gunicorn.conf

echo "Launching supervisor"
sudo supervisorctl update

echo "Application launched"
deactivate
