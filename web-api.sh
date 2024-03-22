fuser -n tcp -k 8765
uwsgi --ini uwsgi.ini --daemonize uwsgi.log --lazy-app