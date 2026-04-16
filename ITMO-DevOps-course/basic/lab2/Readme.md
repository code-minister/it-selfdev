до выходных доделаю, честно 🙏

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

### Шаг 3.0: Пишем манифесты - Namespace
Для создания изолированных сред на одном узле применяются Namespaces. И, хотя их использование оправдано для разделения разных команд, групп или сообществ с разными политиками и ресурсами, почему бы не пощупать его тоже:
```yaml
apiVersion: v1
kind: Namespace
metadata:
  test-environment
```

### Шаг 3.1: Secret
Для начала в кластер нужно перенести необходимые секретные данные, для чего используется сущность Secret. Файл  `db-secret.example`:
```yaml
apiVersion: v1
kind: Secret
metadata: 
  name: postgres-secret
  namespace: dev-environment
type: Opaque
data:
  DB_USER: YWRtaW4=
  DB_PASSWORD: c3VwZXJwYXNzd29yZA==
  DB_NAME: dm90aW5nX2FwcA==
```

### Шаг 3.2: ConfigMap
Используется для хранения разных переменных значений и настроек, тут всё просто:
```yaml
apiVersion: v1
kind: ConfigMap
metadata: 
  name: app-config
  namespace: dev-environment
data:
  DB_PORT: 5432
  BACKGROUND_COLOR: "lightblue"
  BACKEND_URL: "http://backend-service:8080"
```

### Шаг 3.3: 
При созданиии данного манифеста я решил объеденить всё, что касается БД, чтобы не дробить логику слишком сильно. Первым идет StatefulSet, если не ошибаюсь, он полезен при созадании кластеров СУБД, а также повышает надежность данных. Здесь же создаются шалон PVC, который находит или же создают новый PV для конкретной реплики БД. Потом создаётся Headless Service, который не имеет встроенной балансировки и позволяет обращаться к каждому поду сета отдельно. Это важно если у нас есть напрмер разделеие на ReadWrite, ReadOnly etc.
```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: db-app
  namespace: dev-environment
spec:
  serviceName: "db-service"
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:15
        ports:
        - containerPort: 5432
        envFrom:
        - secretRef:
            name: postgres-secret
        volumeMounts:
        - name: db-data
          mountPath: /var/lib/postgresql/data
  volumeClaimTemplates:
    - metadata:
        name: db-data
      spec:
        accessModes: ["ReadWriteOnce"]
        resources: 
          requests:
            storage: 1Gi





---
apiVersion: v1
kind: Service
metadata:
  name: db-service
  namespace: dev-environment
spec:
  type: ClusterIP
  clusterIP: None
  selector:
    app: postgres
  ports:
  - port: 5432
    targetPort: 5432

```






# Источники
- https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/
- https://minikube.sigs.k8s.io/docs/start/?arch=%2Fwindows%2Fx86-64%2Fstable%2F.exe+download
- https://kubernetes.io/docs/tutorials/kubernetes-basics/
- https://kubernetes.io/docs/tasks/administer-cluster/namespaces/#creating-a-new-namespace
- https://www.youtube.com/watch?v=cQkBhGl_hDI
- https://kubernetes.io/docs/concepts/storage/persistent-volumes/
- https://kubernetes.io/docs/concepts/services-networking/service/
- https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/
- 