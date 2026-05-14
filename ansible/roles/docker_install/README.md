# docker_install

Ansible-роль для установки и настройки Docker на Ubuntu 

## Requirements

- Debian/Ubuntu
- systemd
- Python 3
- root privileges

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
| `docker_users` | `list[str]` | `["{{ ansible_user_id }}"]` | Пользователи, добавляемые в группу docker |

## Example

```yaml
- hosts: docker_hosts
  become: true
  roles:
    - docker_install
```

## What the role does

- проверяет, что система относится к Debian-family
- устанавливает Docker и зависимости
- запускает и включает сервис Docker
- добавляет пользователей в группу `docker`
- проверяет установленную версию Docker

## Molecule

Для роли реализованы Molecule-тесты.

Пример запуска:

```bash
cd ansible/roles/docker_install
molecule test -- --ask-pass
```
