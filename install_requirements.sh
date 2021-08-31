#!/bin/sh

sudo su

#Para instalar los paquetes de ubuntu
sudo apt install python3-pip libpq-dev python-dev postgresql curl nginx gunicorn
#Para instalar pgadmin
curl https://www.pgadmin.org/static/packages_pgadmin_org.pub | sudo apt-key add -
sudo sh -c 'echo "deb https://ftp.postgresql.org/pub/pgadmin/pgadmin4/apt/focal pgadmin4 main" > /etc/apt/sources.list.d/pgadmin4.list'
sudo apt update
sudo apt install pgadmin4
#Para instalar los requisitos del proyecto
pip install -r requirements.txt
sudo service nginx start