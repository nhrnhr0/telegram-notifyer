#!/bin/bash
sudo git pull
source /env/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo supervisorctl restart telegramcelery
sudo supervisorctl restart telegramcelerybeat
sudo supervisorctl restart gunicornProj
sudo supervisorctl restart gunicornProjTelegram
sudo service nginx restart
sudo supervisorctl status
echo '=========== done ==========='