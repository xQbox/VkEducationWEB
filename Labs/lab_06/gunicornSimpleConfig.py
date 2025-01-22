bind = "127.0.0.1:8081"

workers = 1

timeout = 30

wsgi_app = "test_wsgi:app"


accesslog = "-"  
errorlog = "-"  
loglevel = "info"
