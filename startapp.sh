IP=$(hostname --all-ip-addresses | awk '{print $1}')
python manage.py runserver 192.168.56.104:9116
