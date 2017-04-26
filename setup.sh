#!/bin/bash

#запускать с sudo из 2017_python
# в конфиге нжинх поменять путь если надо

#sudo -s
add-apt-repository ppa:jonathonf/python-3.6
apt-get update
apt-get install python3.6
pip3 install --upgrade pip
pip3 install --upgrade virtualenv
virtualenv -p python3.6 pestyle
source pestyle/bin/activate
pip3 install django==1.11
easy_install Celery
pip3 install gunicorn
pip3 install Pillow
#библиотека для заполнения базы
pip3 install requests

apt-get install nginx



cp -f ./pestyle_nginx.conf /etc/nginx/sites-available/
ln -s /etc/nginx/sites-available/pestyle_nginx.conf /etc/nginx/sites-enabled/
service nginx restart

python ./msite/manage.py collectstatic

cd ./msite
gunicorn msite.wsgi:application -c ./gunicorn.conf.py

#для запуска отладочного серва джанги и прочая полезная хуйня

#python manage.py createsuperuser
#python manage.py makemigrations pestyle
#python manage.py migrate
#python manage.py runserver
#python -Wall manage.py test
#запуск заполнения базы
#python manage.py fill
#manage.py migrate --database=test_db
