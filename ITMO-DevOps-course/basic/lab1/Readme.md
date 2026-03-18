# Лабораторная №1

## Часть 1

Использовались "Best practices" из следующих источников:
- https://docs.docker.com/build/building/best-practices
- https://habr.com/ru/companies/domclick/articles/546922/
- https://github.com/hadolint/hadolint
- Несветская беседа с парой нейронок

Ознакомившись с паттернами, появилось желание ~~запихнуть~~ включить в один Dockerfile как можно больше из них, чтобы при этом они имели хоть какой-то смысл и были не для галочки. 

### Приложение 
В качестве приложения использовался учебный пример с [docker-curriculum](https://docker-curriculum.com/#our-first-image), переписанный нейронкой с python на компилируемый Go, который должен показывать случайную гифку с котиком на localhost:5000

### "Плохой" Dockerfile
Здесь приведем результаты сборки:

![alt text](images/image.png)

![alt text](images/image-5.png)

![alt text](images/image-3.png)

### "Хороший" Dockerfile
На всякий случай, для чистоты эксперимента, очищаем кэш после предыдущей сборки:
![alt text](images/image-1.png)


Результаты сборки следующие:

![alt text](images/image-2.png)

![alt text](images/image-6.png)

![alt text](images/image-4.png)

Можем заметить, что разница колоссальная. За счёт чего же удалось этого достичь?

### Best Dockerfile practices
---

Немного отклоняясь от задания, буду сразу формулировать как good practices.

#### 1. Многоступенчатая сборка

BAD
```
FROM golang:latest
```

GOOD
```
FROM golang:1.21-bullseye AS builder
...

FROM debian:bullseye-slim
COPY --from=builder /app/cat-app .
```

Позволяет значительно сократить используемое место, так как мы не тащим в итоговый контейнер инструменты сборки, ненужные системные утилиты, а берем только скомпилированный бинарник.

#### 2. Подходящие базовые образы

BAD 
```
FROM golang:latest
```

GOOD
```
FROM debian:bullseye-slim
```

Если бы в этом окошке можно было выделить **slim**, я бы его выделил, а так просто попрошу обратить на него внимание. 

Часто для работы контейнера достаточно довольно урезанной версии базового образа. Отказ от лишнего позволяет сократить размер и уменьшить площадь атаки, ведь чем меньше кода, тем меньше потенциальных уязвимостей. (В нашем случае из-за многоступенчатой сборки пришлось сравнивать разные базовые образы, тем не менее это не делает практику хуже).

#### 3. Указание конкретной версии

BAD 
```
FROM golang:latest

RUN apt install -y fortune-mod
```

GOOD
```
FROM golang:1.21-bullseye

RUN apt-get install -y figlet=2.2.* 
```

Если указать **latest** у базового образа и не указывать версию у пакетов, то скачаются самые актуальные их них. Это может в будущем, при выходе обновлений, привести к конфликтам, если не будет поддерживаться обратная совместимость.

С другой стороны при слишком жесткой фиксации можно пропустить важные фиксы и обновления безопасности. 

Поэтому, как я понял, на практике используют компромисс - фиксируют только мажорную версию, а минорные обновления и патчи берутся самые актуальные.

Либо настроить Docker Scout, чтобы он нас уведомлял, что вышло обновление. Это дает нам больше контроля.


#### 4. Контекст сборки и dockerignore



BAD 
```
COPY . .
```

GOOD
```
COPY app.go .
```

В пределах Dockerfile нужно следить, что мы копируем в рабочую директорию, чтобы, опять же, уменьшить размер и не скопировать случайно чувствительные данные, оин могут обидеться. Мы, допустим, избежали добавления самих Dockerfiles в образ

За пределами Dockerfile, конечно, лучше использовать Dockerignore либо передавать в *docker build* не ".", а только поддиректорию с необходимым для сборки.


#### 5. Rootless контейнеры

BAD 
```
```

GOOD
```
RUN useradd -r catuser

RUN chown catuser:catuser cat-app
USER catuser
```

Так мы значительно уменьшили вероятность получить доступ к нашим секретным ссылкам с котиками, сломать приложение и выйти за пределы контейнера на хост машину.





#### 6. Порядок слоев

BAD 
```
COPY . .

RUN apt update
RUN apt install -y figlet
RUN apt install -y fortune-mod fortunes
```

GOOD
```
RUN apt-get update && apt-get install -y --no-install-recommends \
    figlet=2.2.* \
    fortune-mod \
    fortunes \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /app/cat-app .
```
Слои, которые наименее вероятно будут меняться, стоит ставить в начало, чтобы можно было их не пересобирать, а взять из кэша впоследствии.




#### 7. Сортировка многострочных аргументов


BAD 
```
RUN apt install -y fortune-mod fortunes
```

GOOD
```
RUN apt-get update && apt-get install -y --no-install-recommends \
    figlet=2.2.* \
    fortune-mod \
    fortunes \
    && rm -rf /var/lib/apt/lists/*
```

Это помогает упростить поддержку, обновление списка, пул реквесты и избежать дублирования.


#### 8. Объединение apt-get update && apt-get install
BAD 
```
RUN apt update
RUN apt install -y figlet
```

GOOD
```
RUN apt-get update && apt-get install ...
```
Так как докер кэширует слои, мы можем получить устаревшии версии пакетов, разделяя эти команды


#### 9. Не использовать apt


BAD 
```
RUN apt update
RUN apt install -y figlet
```

GOOD
```
RUN apt-get update && apt-get install ...
```

apt-get считается более надежным для автономного использования.

#### 10. Использовать --no-install-recommends


BAD 
```
RUN apt install -y
```

GOOD
```
RUN apt-get install -y --no-install-recommends
```

Так мы не устанавливаем необязательные пакеты, уменьшая размер образа и поверхность атаки.



### Bad container practices
---

#### 1. Игнорирование лимитов ресурсов

Антипаттерны:

- Не задавать лимиты/requests (в Kubernetes) или ограничения Docker.

Чем плохо: noisy neighbor, непредсказуемая деградация, вынос узла, каскадные падения.


#### 2. Неправильная работа с сетью

Антипаттерны:

- Постоянно использовать --network host “для простоты”.
- Открывать порты без необходимости.
- Смешивать внутренний и внешний трафик без сегментации.

Чем плохо: конфликты портов, сложнее изоляция, труднее безопасность и наблюдаемость.


## Часть 2

В случае с best practices for docker compose file в официальной документации не так много прямых рекомендаций, скорее множество описанных возможностей, поэтому будем больше ссылаться на сторонние ресурсы.

Источники:
- https://dev.to/wallacefreitas/10-best-practices-for-writing-maintainable-docker-compose-files-4ca2
- https://www.youtube.com/watch?v=wSODnwNYglU
- https://www.kapresoft.com/software/2023/10/29/docker-compose-best-practices.html
- Несветская беседа с официальной нейронкой - Гордоном
- Несветская беседа с другими нейронками


### Приложение 

Для демонстрации возьмем учебный пример от [Docker workshop](https://docs.docker.com/get-started/workshop).

### "Плохой" Docker compose file

Сборка представлена на скриншоте:
![alt text](images/image-7.png)




### "Хороший" Docker compose file 

Сборка представлена на скриншоте:
![alt text](images/image-8.png)


### Best Docker compose practices 



#### 1. Healthcheck + depends_on

BAD 
```
```

GOOD
```
  app:
    depends_on:
      mysql:
        condition: service_healthy
  mysql:
    healthcheck:
      test: ["CMD-SHELL", "mysqladmin ping -h 127.0.0.1 -uroot -p$${MYSQL_ROOT_PASSWORD} --silent"]
      interval: 10s
      timeout: 5s
      retries: 10
      start_period: 20s
```

Использование *Healthcheck + depends_on* позволило гарантировать, что приложение, не запустится раньше того сервиса, от которого оно зависит.


#### 2. Переменные окружения

BAD 
```
      MYSQL_HOST: mysql
      MYSQL_USER: root
      MYSQL_PASSWORD: secret
      MYSQL_DB: todos
```

GOOD
```
      MYSQL_HOST: mysql
      MYSQL_USER: ${MYSQL_USER}
      MYSQL_PASSWORD: ${MYSQL_ROOT_PASSWORD}
      MYSQL_DB: ${MYSQL_DB}
```

Если мы не хардкодим секреты, то ниже риск случайно их закоммитить, а также проще поддержка и деплой, ведь они находятся в одном месте.


#### 3. Ограничение ресурсов


BAD 
```
```

GOOD
```
    mem_limit: 512m
    cpus: "1.00"
```

Предотвращает приватизирование всех ресурсов системы одним процессом.



#### 4. Использование Docker Volume 


BAD 
```
```

GOOD
```
services:
  mysql:
    volumes:
      - mysql_data:/var/lib/mysql
...
volumes:
  mysql_data:
```

Сохраняет данные даже при перезапуске или неожиданном сбое контейнера.


### Изоляция контейнеров 

По умолчанию, если явно не указать в каких сетях работают сервисы, они подключаются к сети default, получают соответствующие своим имена в локальной DNS и имеют возможность "достучаться" друг до друга. Однако если явно разделить сервисы по разным сетям они даже не узнают о существовании друг друга.

Добавим следующие элементы в *compose.good.isolated.yaml*:
```
services:
  app:
    networks:
      - app-network

  mysql:
    networks:
      - db-network

networks:
  app-network:
  db-network:
```

После запуска *compose.good.isolated.yaml*,  воспользуемся контейнером nicolaka/netshoot, используемым для работы с сетью, чтобы убедиться что контейнеры действительно не могут знать друг о друге.

Выполним следующие команды:

![alt text](images/image-9.png)

![alt text](images/image-10.png)

![alt text](images/image-11.png)

Видим, что в сети *part-2_app-network* определен ip контейнера с нашим приложением, в отличие от контейнера с базой данных. Ниже может наблюдать обратную ситуацию для сети *part-2_db-network*.

![alt text](images/image-12.png)

![alt text](images/image-13.png)

![alt text](images/image-14.png)

И даже если проверить непосредственно ip-адрес утилитой netcat, подтвердится, что на нём нет никакого mysql:

![alt text](images/image-15.png)






### P.S.

Где-то 25% времени выполнения ЛР ушло на починку Docker на WSL, потому что, как оказалось, он ломается после первого же apt update && apt upgrade. 

Вероятно, проще всё-таки работать в виртуалке..