# container_check

Ansible-роль для проверки Docker-контейнера.

## Requirements

- Ubuntu
- Docker
- root privileges
- Git

## Dependencies

Роль использует следующие внешние коллекции:

- `community.docker`

Для установки зависимостей выполните:

```bash
ansible-galaxy collection install -r requirements.yml
```

## Variables

| Переменная | Тип | Значение по умолчанию | Описание |
|---|---|---|---|
| `app_image_name` | `str` | `"httpstatus"` | Имя Docker image |
| `app_image_tag` | `str` | `"latest"` | Тег Docker image |
| `app_container_name` | `str` | `"httpstatus-check"` | Имя контейнера |
| `app_repo_url` | `str` | `"<repo_url>"` | Git-репозиторий приложения |
| `app_repo_version` | `str` | `"main"` | Ветка/тег репозитория |
| `app_remote_project_path` | `str` | `"/tmp/httpstatus-app"` | Путь проекта на тестовой ВМ |
| `app_dockerfile_path` | `str` | `"docker/Dockerfile"` | Путь до Dockerfile внутри проекта |

## Example

```yaml
- hosts: docker_hosts
  become: true
  roles:
    - container_check
```

## What the role does

- устанавливает git
- клонирует репозиторий приложения
- собирает Docker image
- удаляет старый контейнер
- запускает новый контейнер
- проверяет exit code контейнера
- получает docker logs
- проверяет наличие логов

## Molecule

Для роли реализованы Molecule-тесты.

Пример запуска:

```bash
cd ansible/roles/container_check
molecule test -- --ask-pass --ask-become-pass
```

Для Molecule используется `delegated` driver и отдельная тестовая ВМ.

Перед запуском необходимо:

- иметь SSH-доступ к ВМ;
- указать адрес ВМ в `inventory/inventory.ini`.
