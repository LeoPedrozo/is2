command = '/home/$USER/.local/bin/gunicorn'
pythonpath = '/home/$USER/PycharmProjects/is2'
bind = 'localhost:8000'
workers = 3


#-Para cargar los archivos estaticos
# python manage.py collectstatic
#-Para arrancar gunicorn
# gunicorn -c conf/gunicorn_config.py is2.wsgi
#-Iniciar el servicio nginx
# sudo service nginx start
#-Para detener apache si esta impidiendo a nginx
# sudo apachectl stop
# sudo service apache2 stop