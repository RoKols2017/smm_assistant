[Back to README](../README.md) · [Configuration →](configuration.md)

# Getting Started

## Требования

| Что | Зачем |
|-----|-------|
| Docker + Docker Compose | Основной способ запуска |
| OpenAI API key | Генерация текста и изображений |
| VK user token | Настройка VK и публикация постов с изображением |

## Локальный запуск

```bash
docker compose up --build
```

Для локальной разработки `.env` больше не обязателен: compose подставит dev-defaults. Если хотите управлять секретами и параметрами явно, создайте `.env` из `.env.example` и переопределите значения там.

После старта:

1. Откройте `http://localhost:8000`.
2. Зарегистрируйте пользователя.
3. Войдите в dashboard.
4. Заполните `VK settings`.
5. Перейдите на страницу генерации поста.

Важно: в `VK settings` вставляйте именно `user access token`. Если вставить `ключ сообщества`, текстовая публикация может частично работать, но загрузка изображения на стену обычно будет недоступна.

## Запуск на VPS

```bash
git clone <repository-url>
cd sms_assistant
cp .env.example .env
./deploy_vps.sh
```

Для production перед запуском:

1. заполните `FLASK_SECRET_KEY` и `DATABASE_URL`;
2. положите сертификат и ключ в `/root/cert/<your-domain>/`;
3. во время `./deploy_vps.sh` введите домен, привязанный к VPS;
4. при необходимости смените `NGINX_HTTP_PORT` или `NGINX_HTTPS_PORT`, если `80/443` уже заняты на VPS;
5. при необходимости добавьте `OPENAI_API_KEY`, но отсутствие OpenAI/VK/Telegram не должно ломать сам boot приложения.

Полезные команды:

```bash
docker compose -f docker-compose.yml -f docker-compose.production.yml logs -f nginx web
docker compose -f docker-compose.yml -f docker-compose.production.yml logs -f postgres
docker compose -f docker-compose.yml -f docker-compose.production.yml ps
```

## Что делает bootstrap

При старте production stack:

1. `postgres` поднимается только во внутренней сети;
2. `web` entrypoint ждет готовности PostgreSQL;
3. `web` выполняет `flask --app wsgi.py db upgrade` и запускает Gunicorn на `0.0.0.0:8000`;
4. `deploy_vps.sh` привязывает сертификат и ключ из `/root/cert/<domain>/`;
5. `nginx` публикует внешние порты `80/443`, редиректит трафик на `HTTPS` и проксирует запросы в `web`;
6. healthcheck `nginx` проверяет `http://127.0.0.1/healthz`, а `web` продолжает проверять локальный `http://127.0.0.1:8000/healthz`.

Ожидаемые логи при нормальном старте:

- `[entrypoint] waiting for database availability`
- `[entrypoint] database ready target=...`
- `[entrypoint] database migrations finished`
- `[entrypoint] starting gunicorn bind=... workers=...`
- `nginx ... "GET /healthz HTTP/1.1" 200 ... upstream=web:8000`
- `nginx ... "GET / HTTP/1.1" 301 ...`
- `[main.healthz] completed extra=...`

## Первичная проверка

- открывается страница логина;
- `curl http://localhost/healthz` или `curl http://<VPS-IP>/healthz` возвращает JSON со `status` и `critical_checks`;
- `curl -I https://<your-domain>/` показывает рабочий TLS и ответ приложения;
- регистрация сохраняет пользователя в PostgreSQL;
- dashboard доступен после входа;
- settings сохраняют `vk_api_key` и `vk_group_id`.

## Короткий checklist для первого deploy

1. `docker compose -f docker-compose.yml -f docker-compose.production.yml ps` показывает `postgres`, `web` и `nginx` в состоянии `healthy`.
2. `docker compose -f docker-compose.yml -f docker-compose.production.yml logs -f nginx web` не содержит ошибок про secret key, БД, миграции или upstream `502/504`.
3. `/healthz` через `nginx` возвращает `200 OK`; `optional_providers` могут быть `not_configured` без падения сервиса.
4. Внешний вход идет через `nginx` на `NGINX_HTTP_PORT` или `NGINX_HTTPS_PORT`, а не напрямую в `web`.
5. Session cookie в браузере имеет `Secure` и `HttpOnly` после HTTPS deploy через `./deploy_vps.sh`.

## HTTPS cert layout

`./deploy_vps.sh` ожидает сертификаты в `/root/cert/<domain>/` и пытается автоматически найти одну из типовых пар файлов:

- `fullchain.pem` + `privkey.pem`
- `cert.pem` + `key.pem`
- `certificate.crt` + `private.key`
- `tls.crt` + `tls.key`

## See Also

- [Configuration](configuration.md) — все env-переменные и `DATABASE_URL`.
- [VK Integration](vk-integration.md) — какой VK токен нужен и почему.
- [Architecture](architecture.md) — как устроен Flask app factory.
- [Security](security.md) — ограничения VK token и правила работы с секретами.
