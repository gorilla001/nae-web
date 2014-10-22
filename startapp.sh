IP=$(hostname -I  | awk '{print $1}')
python manage.py runserver ${IP}:8000
