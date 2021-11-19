#!/bin/bash


fab production bootstrap

#return value is 0
if [ $? -eq 0 ]; then
    echo "Iniciando entorno de desarrollo"
    cd /var/www/is2/
    source /var/www/is2/.venv/bin/activate
    #crear la documentacion
    cd /var/www/is2/docs/
    echo "Creando la documentacion"
    make html
    cd ..
    #volver a la carpeta principal

    google-chrome http://127.0.0.1:8000
    python3 manage.py runserver
else
    echo "Iniciando entorno de produccion"
    cd /var/www/is2/
    source /var/www/is2/.venv/bin/activate
    #crear la documentacion
    cd /var/www/is2/docs/
    echo "Creando la documentacion"
    make html
    cd ..
    #volver a la carpeta principal
    google-chrome http://127.0.0.1:8000
    gunicorn -c conf/gunicorn_config.py is2.wsgi
fi
