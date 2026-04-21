# SMM Assistant

> Flask-приложение для генерации SMM-постов, изображений и автопубликации в VK с хранением пользователей в PostgreSQL.

Проект превращает первую часть учебного репозитория в веб-приложение: регистрация и вход, пользовательские VK-настройки, генерация контента через OpenAI и базовая VK-статистика в одном Docker-ready сервисе. Для VPS поддерживается production override со схемой `nginx -> web -> postgres`.

## Быстрый старт

```bash
docker compose up --build
```

После запуска приложение доступно на `http://localhost:8000`.

`docker compose` теперь имеет dev-defaults и может стартовать без `.env`. Если нужен production-like или кастомный запуск, сначала создайте `.env` из `.env.example`.

## Что умеет MVP

- **Регистрация и вход**: обычная сессионная auth на Flask.
- **Пользовательские VK settings**: хранение token и group id в PostgreSQL.
- **Генерация поста**: `tone`, `topic`, генерация текста и изображения.
- **Автопостинг в VK**: выполняется best-effort и не ломает генерацию при отказе VK.
- **VK Stats**: минимум число подписчиков группы.

## Docker Compose на VPS

```bash
cp .env.example .env
docker compose -f docker-compose.yml -f docker-compose.production.yml up -d --build
docker compose -f docker-compose.yml -f docker-compose.production.yml logs -f nginx web
```

Для production обязательно задайте как минимум:

- `FLASK_SECRET_KEY`
- `DATABASE_URL`
- `TRUST_PROXY_COUNT=1` для встроенного `nginx`
- `NGINX_HTTP_PORT`

После старта production stack должен:

1. поднять `postgres` во внутренней сети;
2. дождаться PostgreSQL в контейнере `web` и выполнить `flask --app wsgi.py db upgrade`;
3. поднять Gunicorn только во внутренней сети;
4. поднять `nginx` на внешнем HTTP порту;
5. отвечать `200 OK` на `GET /healthz` через `nginx`.

Типичные полезные логи production-контейнеров:

- `nginx ... "GET /healthz HTTP/1.1" 200 ... upstream=web:8000`
- `[entrypoint] waiting for database availability`
- `[entrypoint] database ready ...`
- `[entrypoint] database migrations finished`
- `[entrypoint] starting gunicorn ...`
- `[main.healthz] completed ...`

Если startup падает, первым делом проверьте `docker compose -f docker-compose.yml -f docker-compose.production.yml logs -f nginx web` на ошибки про `FLASK_SECRET_KEY`, `DATABASE_URL`, миграции, upstream `502/504` или недоступную БД.

## Важная оговорка по VK

Для разных VK-сценариев нужны разные типы токенов:

- `group/community token` подходит только для части server-side сценариев и может не дать загрузить изображение на стену;
- `user access token` нужен для полноценного автопостинга с изображением;
- наличие scope `wall, photos` само по себе не гарантирует успех: важен еще тип токена и реальные права пользователя в сообществе.

Если токен подходит только для текста, приложение опубликует пост без изображения и покажет предупреждение вместо полного отказа.

## Документация

| Руководство | Описание |
|-------------|----------|
| [Getting Started](docs/getting-started.md) | Локальный запуск и первый вход |
| [Configuration](docs/configuration.md) | Env-переменные Flask, OpenAI и Postgres |
| [VK Integration](docs/vk-integration.md) | Какие VK токены нужны и почему |
| [Architecture](docs/architecture.md) | Структура Flask modular monolith |
| [Testing](docs/testing.md) | Тесты, smoke-check и статические проверки |
| [Security](docs/security.md) | Секреты, пароли и ограничения VK token |

## Ключевые файлы

- `wsgi.py` — WSGI entrypoint для Gunicorn.
- `app/__init__.py` — Flask app factory.
- `docker-compose.yml` — локальный `web + postgres` стек.
- `docker-compose.production.yml` — production override с `nginx`.
- `docker/entrypoint.sh` — ожидание БД и запуск `flask db upgrade`.
- `docker/nginx/` — конфиги и каталоги reverse proxy.

## Лицензия

MIT License.
