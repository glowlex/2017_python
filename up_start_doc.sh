docker pull glowlex/pestyle
docker run -v /opt/project/2017_python/msite/pestyle/static:/var/www/static -v /opt/project/2017_python/prod_db.sqlite3:/var/www/sql/db.sqlite3  -t -p 80:80 glowlex/pestyle
