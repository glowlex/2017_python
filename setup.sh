#!/bin/bash

#запускать с sudo
# в конфиге нжинх поменять путь если надо

#sudo -s
add-apt-repository ppa:jonathonf/python-3.6
apt-get update
apt-get install python3.6
pip3 install --upgrade pip
pip3 install --upgrade virtualenv
virtualenv -p python3.6 pestyle
source pestyle/bin/activate
pip3 install django==1.10.6
easy_install Celery
pip3 install gunicorn
apt-get install nginx


#rm /etc/nginx/sites-enabled/pestyle_nginx.conf
cp -f ./pestyle_nginx.conf /etc/nginx/sites-available/
ln -s /etc/nginx/sites-available/pestyle_nginx.conf /etc/nginx/sites-enabled/
service nginx restart

python ./msite/manage.py collectstatic

cd ./msite
gunicorn msite.wsgi:application

#для запуска отладочного серва джанги
#python manage.py createsuperuser
#python manage.py migrate
#python manage.py runserver
