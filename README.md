# Dannyset
Установите python, flask и модули. 
```bash
sudo apt install python3 python3-flask python3-pip
sudo pip3 install werkzeug requests
sudo apt install nginx gunicorn
```
Скопируйте содержимое файла app.py в главный файл приложения. Измените ip на ip своей машины.
Скопируйте содержимое файла run.py, если меняли имя главного файла, измените его и тут.
Создайте server.service командой:
```bash
sudo nano /etc/systemd/system/server.service
```
и скопируйте в него содержимое соответствующего файла. Подправьте пути и имена.
Создайте страницу в nginx 
```bash
sudo nano /etc/nginx/sites-available/server
```
Cкопируйте туда содержимое server.

Проверьте service файл. Введите 
```bash
sudo systemctl start server
```
если вы сделали все правильно, в папке приложения должен появится сокет файл.
Сделайте символическую ссылку на nginx файл 
```bash
sudo ln -s /etc/nginx/sites-available/server /etc/nginx/sites-enabled/server
```
Проверьте конфигурацию 
```bash
nginx sudo nginx -t
```
Если все прошло успешно, перезапустите nginx: 
```bash
sudo service nginx restart
```
Добавьте server в автозагрузку, чтобы сервер автоматически запускался. 
```bash
sudo systemctl enable server
```


## Склонируйте репозиторий

```bash 
git clone https://github.com/Danny1234561111/Dannyset.git
```
