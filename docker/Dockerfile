FROM python:3.6


COPY ./requirements.txt ./msite ./docker/src/settings.py ./docker/src/pestyle_nginx.conf /opt/project/

WORKDIR /opt/project/

RUN apt-get update && apt-get install -y openssh-server \
&& apt-get install -y nginx \
&& pip3 install -r ./requirements.txt

RUN cp -f ./pestyle_nginx.conf /etc/nginx/sites-available/ \
&& ln -s /etc/nginx/sites-available/pestyle_nginx.conf /etc/nginx/sites-enabled/ \
&& mkdir /var/www/static \
&& cp -f ./settings.py ./msite/settings.py


WORKDIR /opt/project/

ENTRYPOINT service nginx start && gunicorn msite.wsgi:application -c ./gunicorn.conf.py
#ENTRYPOINT ["gunicorn"]
#CMD ["msite.wsgi:application", "-c", "./gunicorn.conf.py"]


#EXPOSE 8080
