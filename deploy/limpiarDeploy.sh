#!/bin/bash

sudo rm /etc/supervisor/conf.d/celeryd.conf
sudo rm /etc/supervisor/conf.d/celerycam.conf
sudo rm /etc/supervisor/conf.d/celerybeat.conf
sudo rm /etc/supervisor/conf.d/is2.conf
sudo rm -rf /var/www/is2/
sudo rm /etc/nginx/sites-enabled/is2.conf