#!/bin/bash
sudo apt install cron -y
python3 -m pip install -r requirements.txt
py_install_file="install.py"

# Get current fullpath
fullpath=$(readlink -f "$0")
# Extract directory path 
dirPath=$(dirname "$fullpath")

# Run install.py
py_install_path="$dirPath/$py_install_file"
python3 $py_install_path
crontab_config_file="crontab.config" 
crontab_config_path="$dirPath/$crontab_config_file"
crontab $crontab_config_path
sudo systemctl restart cron
sudo systemctl enable cron

