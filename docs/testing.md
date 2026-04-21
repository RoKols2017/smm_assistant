[← Architecture](architecture.md) · [Back to README](../README.md) · [Security →](security.md)

# Testing

## Что проверяется

- app factory и регистрация routes;
- регистрация/логин пользователя;
- сохранение VK settings;
- content workflow и graceful degradation при проблемах VK.

## Тесты

```bash
python -m pytest tests/ -v
```

Для docker integration smoke-check с `nginx` можно запускать отдельный integration-тест:

```bash
python -m pytest tests/integration/test_deploy_stack.py -m integration -v
```

## Статическая проверка синтаксиса

```bash
python -m compileall app config.py generators social_publishers social_stats
```

## Docker smoke-check

После настройки окружения:

```bash
docker compose up --build
docker compose logs -f web
```

`.env` для dev smoke-check не обязателен: compose подставит безопасные значения по умолчанию. Для сценариев, близких к production, используйте явный `.env`.

Дополнительно проверьте, что в логах `web` есть успешный `db upgrade`, а не откат на bootstrap-режим.

## Production-like smoke-check with nginx

```bash
./deploy_vps.sh
docker compose -f docker-compose.yml -f docker-compose.production.yml ps
curl http://127.0.0.1:${NGINX_HTTP_PORT:-80}/healthz
curl -kI https://127.0.0.1:${NGINX_HTTPS_PORT:-443}/
docker compose -f docker-compose.yml -f docker-compose.production.yml logs -f nginx web
```

Ожидаемое поведение:

- `nginx` и `web` оба становятся `healthy`;
- `/healthz` отвечает через `nginx`, а не напрямую из `web`;
- `https://...` отвечает через `nginx` с подключенным сертификатом;
- в логах `nginx` нет постоянных `502`/`504`;
- в логах `web` есть `[main.healthz] completed`.

## Текущее ограничение локального окружения агента

В текущем рабочем окружении системный Python был без `pip`, поэтому во время этой сессии полноценный runtime-прогон Flask/pytest локально не выполнялся. Для проекта это компенсируется Docker-сценарием, который устанавливает зависимости внутри контейнера.

## See Also

- [Getting Started](getting-started.md) — основной запуск.
- [Configuration](configuration.md) — env-переменные для тестового и Docker запуска.
- [VK Integration](vk-integration.md) — какие VK capability нужно проверять вручную.
- [Architecture](architecture.md) — какие слои покрываются тестами.
