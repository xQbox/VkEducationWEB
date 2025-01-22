import multiprocessing

bind = '127.0.0.1:8000'
workers = multiprocessing.cpu_count() * 2 + 1
threads = 2

timeout = 30

wsgi_app = "askme_rodinkov.wsgi:application"

accesslog = "-" #stdout
errorlog = '-' #stderr
loglevel = "info"

worker_connections = 1000

pidfile = "./gunicorn_askme_rodinkov.pid" # PID для процесса родителя для workers
