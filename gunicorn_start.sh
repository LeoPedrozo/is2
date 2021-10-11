sudo service nginx start
gunicorn -c conf/gunicorn_config.py is2.wsgi

#gunicorn --bind 127.0.0.1:8000 is2.wsgi
#Si nginx falla al iniciar utilizar el siguiente comando
#sudo apachectl stop

#Para probar el funcionamiento de nginx
#sudo nginx -t

#Para reiniciar el servicio
#sudo service nginx restart