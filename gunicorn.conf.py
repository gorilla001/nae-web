'''
[program:jmpush]
command=/home/sysop/.virtualenvs/%(program_name)s/bin/gunicorn %(program_name).wsgi:application -c /home/www/%(program_name)s/gunicorn.conf.py
user=sysop
directory=/home/www/%(program_name)s
autostart=true
autorestart=true
redirect_stderr=True
'''


workers = 5
worker_class = "gevent"
bind = "127.0.0.1:9116"
chdir = "/home/www/jaeweb"
