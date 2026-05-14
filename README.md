# HTTP Status Checker

Проект состоит из трёх частей:

1. Python-скрипт для проверки HTTP-статусов
2. Docker-образ для запуска скрипта в контейнере
3. Ansible-автоматизация установки Docker и проверки контейнера

## Структура проекта

```text
.
├── script/
│   ├── check_status.py
│   └── requirements.txt
├── docker/
│   ├── Dockerfile
│   └── requirements.txt
└── ansible/
    ├── README.md
    ├── playbooks/
    ├── inventory/
    └── roles/
```

## 1. Python-скрипт

Скрипт `script/check_status.py` отправляет HTTP-запросы к сервису, который возвращает указанный HTTP-статус.

По умолчанию используется сервис:

```text
https://tools-httpstatus.pickup-services.com
```

Скрипт проверяет несколько кодов ответа:

```text
100, 200, 302, 404, 500
```

Для каждого запроса выводится лог с URL, статусом ответа и телом ответа.

### Флаги

Поддерживаются следующие флаги:

| Флаг | Описание |
|---|---|
| `--url` | Позволяет указать базовый URL сервиса |
| `--random` | Отправляет 5 запросов со случайными HTTP-кодами |

Флаг `--url` добавлен, потому что основной сервис может быть временно недоступен. В таком случае можно передать другой сервис, например:

```bash
python3 script/check_status.py --url https://mock.codes
```

Запуск со случайными кодами:

```bash
python3 script/check_status.py --random
```

### Зависимости

Для работы скрипта используется библиотека:

```text
requests
```

Установка зависимостей:

```bash
pip install -r script/requirements.txt
```

---

## 2. Docker

Для запуска скрипта в контейнере написан `Dockerfile`.

Docker-образ:

- использует официальный образ `ubuntu:22.04`
- устанавливает Python и необходимые зависимости
- создаёт виртуальное окружение
- устанавливает зависимости из `requirements.txt`
- копирует Python-скрипт внутрь контейнера
- запускает скрипт при старте контейнера
- запускает приложение не от root-пользователя

### Сборка образа

Из корня проекта:

```bash
docker build -f docker/Dockerfile -t httpstatus .
```

### Запуск контейнера

```bash
docker run --name httpstatus-container httpstatus
```

### Просмотр логов

```bash
docker logs httpstatus-container
```

### Повторный запуск

Если контейнер уже существует, его можно удалить:

```bash
docker rm httpstatus-container
```

И запустить заново:

```bash
docker run --name httpstatus-container httpstatus
```

---

## 3. Ansible

Ansible используется для автоматизации установки Docker и проверки работы контейнера на целевом хосте

Реализованы две роли:

| Роль | Назначение |
|---|---|
| `docker_install` | Устанавливает Docker, добавляет пользователя в группу `docker`, запускает и включает `docker.service` |
| `container_check` | Собирает Docker-образ, запускает контейнер, проверяет exit code и выводит результат через `docker logs` |

Playbook автоматизирует:

- установку Docker
- проверку установки Docker
- сборку Docker image
- запуск контейнера
- проверку корректного завершения контейнера
- получение и вывод `docker logs` через Ansible

Подробное описание Ansible-части находится в отдельном [файле](ansible/README.md)
