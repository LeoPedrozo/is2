touch /etc/nginx/sites-available/is2
sudo su
cat nginx_conf.txt >> /etc/nginx/sites-available/is2
cd /etc/nginx/sites-enabled/
ln -s /etc/nginx/sites-available/is2
sudo systemctl restart nginx