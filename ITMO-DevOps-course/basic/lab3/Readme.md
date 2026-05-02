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


# Вместо вывода
Во-первых, я [настроил](https://code.visualstudio.com/docs/languages/markdown#_inserting-images-and-links-to-files) чтобы при вставке картинки автоматически падали в директорию images. И я очень рад.
Во-вторых ...


# Источники
- https://nginx.org/ru/linux_packages.html
- 