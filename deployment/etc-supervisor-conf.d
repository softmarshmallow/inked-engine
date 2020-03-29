
[program:asgi_daphne]

directory=/home/ubuntu/app/inked-engine/

command=/home/ubuntu/app/inked-engine/venv/bin/daphne --bind 0.0.0.0 --port 8001 server.asgi:application
# 0.0.0.0 ip of your website
# I choose the port 8000 for daphne

stdout_logfile=/var/log/daphne.log

autostart=true

autorestart=true

redirect_stderr=true



