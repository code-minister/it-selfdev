До выходных сделаю 🙏
# Лабораторная №3

## Часть 1

К этой лабе подход тот же, просим нейронку придумать проект, чтобы пощупать побольше возможностей nginx.

### Приложение 

Очень кратко, сайт-визитка с апишкой. Используемые фичи:
- Виртуальные хосты
- HTTPS и редиректы
- Reverse Proxy и Балансировка
- Кэширование
- Безопасность
- Управление путями
- Логирование 


### Шаг 0: Установка
Устанавливаем по крутому из официального репозитория с проверкой ключа:
```shell
sudo apt install curl gnupg2 ca-certificates lsb-release ubuntu-keyring

curl https://nginx.org/keys/nginx_signing.key | gpg --dearmor \
    | sudo tee /usr/share/keyrings/nginx-archive-keyring.gpg >/dev/null

gpg --dry-run --quiet --no-keyring --import --import-options import-show /usr/share/keyrings/nginx-archive-keyring.gpg | grep 573BFD6B3D8FBC641079A6ABABF5BD827BD9BF62

echo "deb [signed-by=/usr/share/keyrings/nginx-archive-keyring.gpg] \
https://nginx.org/packages/ubuntu `lsb_release -cs` nginx" \
    | sudo tee /etc/apt/sources.list.d/nginx.list

echo -e "Package: *\nPin: origin nginx.org\nPin: release o=nginx\nPin-Priority: 900\n" \
    | sudo tee /etc/apt/preferences.d/99nginx

sudo apt update
sudo apt install nginx
```

### Шаг 1: Проект и настройка путей
Чтобы удобно работать с файлами из VS Code сделаем следующее:
1. Создаем бэкап исходного конфига, а вместо него создаем ссылку на файл в нашей директории
```bash
sudo mv /etc/nginx/nginx.conf /etc/nginx/nginx.conf.backup
sudo ln -s /home/arthur/it-selfdev/ITMO-DevOps-course/basic /etc/nginx/nginx.conf
```
2. В начале конфигурационного файла записываем `user arthur;`, чтобы у процесса был доступ к файлам директории.


### Шаг 2: Настройка переадресации
> Пока что комментируем базовые настройки
Создаем контекст директиву http, в её контексте - server. Это будет наш первый виртуальный дефолтный сервер для порта 80, который редиректит на https по тому же URL
```nginx
    server {
        listen 80 default_server;
        server_name _;
        return 301 https://$host/$request_uri;
        }
```

### Шаг 3.1: Создание SSL сертификата и настройка HTTPS
Так как мы работаем на локалке, воспользуемся утилитой openssl. И так как у нас несколько доменов, настроим SAN (Subject Alternative Name).
```bash
sudo mkdir -p /etc/ssl/private /etc/ssl/certs
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/nginx-selfsigned.key -out /etc/ssl/certs/nginx-selfsigned.crt -addext "subjectAltName=DNS:portfolio.local,DNS:api.portfolio.local"
```

Далее настраиваем https:
```nginx
http{
    ssl_certificate     /etc/ssl/certs/nginx-selfsigned.crt;
    ssl_certificate_key /etc/ssl/private/nginx-selfsigned.key;

    server {
        listen 443 ssl;
        ...
    }
}
```

### Шаг 3.2: Оптимизация HTTPS
SSL handshake достаточно ресурсозатратная операция, поэтому давайте оптимизируем её с помощью использования постоянных соединений (по умолчанию активно, но пропишем явно) и сохранения параметров SSL-сессии.
```nginx
http {
    ssl_certificate     /etc/ssl/certs/nginx-selfsigned.crt;
    ssl_certificate_key /etc/ssl/private/nginx-selfsigned.key;

    ssl_session_cache   shared:SSL:10m;
    ssl_session_timeout 10m;

    keepalive_timeout 75s

}
```

Эти настройки будут применятся ко всем создаваемым далее серверам.



# Вместо вывода
Во-первых, я [настроил](https://code.visualstudio.com/docs/languages/markdown#_inserting-images-and-links-to-files) чтобы при вставке картинки автоматически падали в директорию images. И я очень рад.
Во-вторых ...


# Источники
- https://nginx.org/ru/linux_packages.html
- https://nginx.org/ru/docs/http/configuring_https_servers.html