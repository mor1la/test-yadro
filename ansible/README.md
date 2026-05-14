# Ansible

Были реализованы роли:

- `docker_install` — установка и настройка Docker
- `container_check` — сборка и проверка Docker-контейнера

Также реализовано тестирование ролей с использованием **Molecule**.

## Структура проекта

| Роль | Описание | Ссылка |
|---|---|---|
| `docker_install` | Установка и настройка Docker | [README.md](ansible/roles/docker_install/README.md) |
| `container_check` | Сборка и проверка Docker-контейнера | [README.md](ansible/roles/container_check/README.md) |

---

## Inventory

Используется inventory:

```ini
[local]
localhost ansible_connection=local ansible_user=marina

[vm]
test-vm ansible_host=YOUR_VM_IP ansible_user=root

[docker_hosts:children]
local
vm

[all:vars]
ansible_python_interpreter=/usr/bin/python3
```

Для тестирования на своей ВМ необходимо заменить:

```ini
ansible_host=YOUR_VM_IP
```

на IP-адрес своей ВМ.

## Установка зависимостей

Установка Ansible collections:

```bash
ansible-galaxy collection install -r requirements.yml
```

## Локальный запуск playbook

```bash
ansible-playbook playbooks/main.yml --limit local
```

---

## Запуск playbook на ВМ

```bash
ansible-playbook playbooks/main.yml --limit vm --ask-pass
```

---

## Molecule

Для ролей реализованы Molecule-тесты.

### Пример запуска тестов

```bash
cd ansible/roles/docker_install
molecule test -- --ask-pass 
```

```bash
cd ansible/roles/container_check
molecule test -- --ask-pass 
```

Используется Molecule `delegated` driver. Тесты выполняются на отдельной ВМ. Перед запуском необходимо указать свою ВМ в `inventory/inventory.ini`.

В процессе реализации рассматривалось два варианта тестирования:

- запуск Molecule через Docker `(docker-in-docker)`
- тестирование на отдельной ВМ через `delegated driver`

В итоге был выбран вариант с отдельной ВМ, так как он ближе к реальному окружению, позволяет тестировать установку Docker и запуск контейнеров в полноценной системе, а также избегает ограничений и особенностей docker-in-docker.

## SSH
Для работы Ansible используется SSH-подключение.
Возможны два варианта:

- аутентификация по паролю
- аутентификация по SSH-ключу

## Функциональность
Плейбук автоматизирует:

- установку Docker
- настройку Docker
- сборку Docker image
- запуск контейнера
- проверку exit code контейнера
- проверку docker logs
- тестирование ролей через Molecule