#!/bin/sh
#Para migrar la base de datos
python3 manage.py migrate gestionUsuario
python3 manage.py makemigrations
python3 manage.py migrate gestionUsuario
python3 manage.py migrate

python3 manage.py createsuperuser

#Para borrar permisos remanentes de modelos que ya no existen
# python3 manage.py remove_stale_contenttypes
