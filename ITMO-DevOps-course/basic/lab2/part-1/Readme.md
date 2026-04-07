# Лабораторная №1

> Работа выполнялась на Minikube, установленный на WSL

## Часть 1

Итак, к этой лабе я тоже решил подойти проактивно и попробовать "пощупать" как можно больше базовых возможностей и абстракций кубера.

### Приложение
Для данной работы нейронкой было придумано приложение для голосования, состоящее из 4 частей: backend, frontend, bd и worker (скрипт, периодически подводящий промежуточные итоги). При чем общение с беком проходит через фронт. Такой подход поможет сфокусироваться на изучении DevOps инструментов, а не на написании кода приложения.

### Шаг 1: Контейнеризация 
Не перестаем практиковаться, для каждого компонента (части) были ручками написаны Dockerfile и .dockerignore. Также для полного теста и последующего деплоя был написан compose file.

### Шаг 2:Деплой 
Благодаря тому, что в compose.yaml мы используем атрибуты build + image, мы можем запушить необходимые образы в наш реестр командой ```docker compose push```

### Шаг 3.1: Пишем манифесты - Secret
Для начала в кластер нужно перенести необходимые секретные данные, для чего используется сущность Secret. Файл  `db-secret.example`:
```
apiVersion: v1
kind: Secret
metadata: 
  name: postgres-secret
type: Opaque
data:
  DB_USER: YWRtaW4=
  DB_PASSWORD: c3VwZXJwYXNzd29yZA==
  DB_NAME: dm90aW5nX2FwcA==
```

### Шаг 3.2:



# Источники
- https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/
- https://minikube.sigs.k8s.io/docs/start/?arch=%2Fwindows%2Fx86-64%2Fstable%2F.exe+download
- https://kubernetes.io/docs/tutorials/kubernetes-basics/
- https://www.youtube.com/watch?v=cQkBhGl_hDI