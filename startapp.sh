IP=$(hostname --all-ip-addresses | awk '{print $1}')
python manage.py runserver ${IP}:9116
