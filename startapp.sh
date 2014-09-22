IP=$(ifconfig enp0s3 | grep -w inet | awk '{print $2}')
python manage.py runserver ${IP}:8000
