#!/bin/bash
sudo su
apt install cron
python3 -m pip install -r requirements.txt
python3 install.py

# Get current fullpath
fullpath=$(readlink -f "$0")
# Extract directory path 
dirPath=$(dirname "$fullpath")
crontab_config_file="crontab.config" 
crontab_config_path="$dirPath/$crontab_config_file"
crontab $crontab_config_path
sudo systemctl restart cron
sudo systemctl enable cron

