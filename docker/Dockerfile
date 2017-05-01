FROM python:3.6


COPY ./src/requirements.txt ./src/msite ./src/settings.py /opt/project/

#почему то ворк дир не работает
RUN cd /opt/project/ && apt-get update && apt-get install -y openssh-server \
&& apt-get install -y nginx \
&& ln -s /etc/nginx/sites-available/pestyle_nginx.conf /etc/nginx/sites-enabled/ \
&& mkdir /var/www/static \
&& cp -f ./settings.py ./msite/settings.py \
&& pip3 install -r ./requirements.txt



#EXPOSE 8080
