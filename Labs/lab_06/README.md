# Лабораторная работа N6
## Настройка nginx
### Зависимости : django, ipython, django-bootstrap-v5, gunicorn, Faker """ pip install Faker """, Pillow """ pip install Pillow """, nginx 'sudo apt install nginx' 
#### Скрипты запуска ( директория lab_06 ) :  
#### Задание 1 wsgi 2 workers -> gunicorn -c ./app/gunicorn.conf.py
#### Задание 2 wsgi POST GET -> gunicorn -c gunicornSimpleConfig.py  (chmod +x testGet.sh, chmod +x testPost.sh) or http://127.0.0.1:8081/?name=Aleksei&prof=football - GET ; curl -X POST -d "key1=value1&key2=value2" http://127.0.0.1:8081/ - POST
#### Задание 3 NGINX : 
- { sudo systemctl status nginx - получить статус  or curl http://localhost/nginx_status ; 
- sudo systemctl restart nginx - перезапуск nginx; curl -I http://localhost/ } 
- Этапы установить nginx; 
- UNIX скопировать файл ask_rodinkov.conf и proxnginx.conf в директорию /etc/nginx/sites-avaliable/
- sudo ln -s /etc/nginx/sites-available/ask_rodinkov.conf /etc/nginx/sites-enabled/
- sudo nginx -t ; sudo systemctl restart nginx
- Запустить пункт 2
- Открыть sample.html 
- получить 1.png
#### Задание 4 NGINX : 
- Выполнить 3 (за исключением sudo ln -s /etc/nginx/sites-available/proxnginx.conf /etc/nginx/sites-enabled/)
