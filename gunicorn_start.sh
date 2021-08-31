sudo service nginx start
gunicorn -c conf/gunicorn_config.py is2.wsgi