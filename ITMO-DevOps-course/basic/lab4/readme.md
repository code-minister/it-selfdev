# Лабораторная №4

Начав обозревать тему CI\CD, создалось ощущение, что она является наиболее объёмной из курса, так как пайплайн может значительно отличаться в зависимости от принятых в компании практик, бизнес-процессов, методологий, архитектуры самого продукта и тд. 

> Но и в этот раз сделаю качественно и по красоте.

## Часть 1

> Для настройки CI\CD использовался GitHub Actions

### Приложение 

Для тестов возьмем проект из ЛР№2 - небольшой сайт для голосования, с настроенным HELM'ом, однако будем использовать k3s так как minikube потребляет больше ресурсов и не подходит для запуска в VM. Работа будет реализована на VM Ubuntu-server 24.04.

### Pipeline

Для симуляции работы CI\CD создадим два окружения: test и prod, где деплой во второе будет требовать подтверждения. Окружения будем разделять по namespace в helm и поддомену test. Раннер будет запущен локально

> Написать про этапы

### Шаг 0: Настройка VM
Для проекта было выделено 7 Гб RAM и 6 ядер ЦПУ, настройка выполнялась автоматически. Для удобства работы настроим подключение по SSH, для этого пробросим 22 порт в настройках VM (Расширенные -> Сеть -> Проброс портов -> Добавить новое правило)
![alt text](images/image.png)

Теперь к VM можно подключиться командой
```bash
ssh -p 2222 username@127.0.0.1
```

### Шаг 1.1: Установка зависимостей
#### Docker
```bash
# Add Docker's official GPG key:
sudo apt update
sudo apt install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/docker.asc
EOF

sudo apt update

sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

####  k3s
```bash
curl -sfL https://get.k3s.io | sh -
```

### Шаг 1.1: Настройка окружения
#### Пользователь gha
```bash
sudo useradd -m -s /bin/bash gha-runner
sudo passwd gha-runner
```

#### Docker
```bash
sudo usermod -aG docker gha-runner
newgrp docker
```
#### k3s
```bash
sudo -u gha-runner mkdir -p /home/gha-runner/.kube
sudo cp /etc/rancher/k3s/k3s.yaml /home/gha-runner/.kube/config
sudo chown gha-runner:gha-runner /home/gha-runner/.kube/config
sudo chmod 600 /home/gha-runner/.kube/config
```


### Шаг 2: Настраиваем self-hosted runner
Переходим Settings -> Actions -> Runners -> New self-hosted runner
Выбираем Linux x64
#### Download
```bash
su - gha-runner

mkdir actions-runner && cd actions-runner
curl -o actions-runner-linux-x64-2.334.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.334.0/actions-runner-linux-x64-2.334.0.tar.gz
echo "048024cd2c848eb6f14d5646d56c13a4def2ae7ee3ad12122bee960c56f3d271  actions-runner-linux-x64-2.334.0.tar.gz" | shasum -a 256 -c
tar xzf ./actions-runner-linux-x64-2.334.0.tar.gz
```
#### Configure
```bash
./config.sh --url https://github.com/code-minister/it-selfdev --token A7YMG7G4Y25NQEZQPF6Y35DKCRN4W
./run.sh
```
#### Автоперезапуск 
```bash
su -
cd /home/gha-runner/actions-runner/

./svc.sh install
./svc.sh start
```

### Шаг 3



# Источники
- https://docs.docker.com/engine/install/ubuntu/
- https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/add-runners
- 