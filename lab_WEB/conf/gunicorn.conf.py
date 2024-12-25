import multiprocessing

bind = "127.0.0.1:8080"
workers = multiprocessing.cpu_count()

accesslog = '/var/tmp/askme/access.log'
errorlog = '/var/tmp/askme/error.log'
